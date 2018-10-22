# Standard library imports
import time
import re
import os
import subprocess
import shutil
import shlex
import tempfile

# Third-party imports
import numpy


from lib.mock_drs import MockDRS
import cdms2 as cdms


# Define CDO path
cdo_path = "/usr/bin/cdo"


def _validate_input_grid(input_file):

    tmp_file = tempfile.mktemp()
    cmd = "%s timmean -seltimestep,1 %s %s" % (cdo_path, input_file, tmp_file)

    # Run the CDO process
    proc = subprocess.Popen(shlex.split(cmd), stderr=subprocess.PIPE, stdout=subprocess.PIPE, env=os.environ)
    retvals = proc.communicate()
    outputs = {"stdout": retvals[0], "stderr": retvals[1], "returncode": proc.returncode}

    # Analyse the output for the error "generic" meaning that cdo does not recognise the grid which may mean
    # that the file contains no fields, just a time series
    if outputs["stderr"].replace("\n", "").find("generic") > -1:
        raise Exception(
            "No spatial grid in this dataset or not recognised grid. Please check the grid in the dataset.")


def regrid(input_file, domain_type, output_base_dir='OUT'):
    # Define some rules regarding the inputs and how they map to information needed by this process
    if domain_type == "global":
        grid_definition_file = "./grid_files/ll1deg_grid.nc"
        grid_short_name = "1-deg"
        output_dir = os.path.join(output_base_dir, "1_deg")
    else:
        regional_domain = os.path.basename(input_file).split("_")[1]
        grid_definition_file = "./grid_files/ll0.5deg_%s.nc" % regional_domain
        grid_short_name = "0.5-deg"
        output_dir = os.path.join(output_base_dir, "0.5_deg")

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    # Validate input grid first - check CDO can manage it
    _validate_input_grid(input_file)

    # Determine output file name
    output_file_name = os.path.split(input_file)[1]
    output_file = os.path.join(output_dir, output_file_name)

    # We will need to select the main variable using the "select" operator piped into the CDO operator
    var_id = os.path.basename(input_file).split("_")[0]

    if domain_type == "global":
        operation = "setgridtype,lonlat -remapbil,%s -select,name=%s" % (grid_definition_file, var_id)
    else:
        operation = "remapbil,%s -select,name=%s" % (grid_definition_file, var_id)

    # Get the variable (in external file) that contains the grid cell area variable
    cell_areas_file = _getGridCellAreaVariable(var_id, input_file)

    if cell_areas_file:
        operation += " -setgridarea,%s" % cell_areas_file

    options = ("-b F64",)
    outputs = _cdoWrapper(operation, [input_file], output_file)

    validate_regridded_file(output_file, domain_type)

    if domain_type == "regional":
        # Convert to NetCDF 3
        tmp_file = output_file[:-3] + "-tmp.nc"
        os.system("/usr/bin/ncks -3 %s %s" % (output_file, tmp_file))
        os.system("mv %s %s" % (tmp_file, output_file))
        print("Converted to NetCDF3 file: %s" % output_file)

    return output_file


def validate_regridded_file(input_file, domain_type):
    outputs = _cdoWrapper("sinfo", [input_file], "")

    if domain_type == "global":
        if not outputs["stdout"].find("points=64800 (360x180)") > -1:
            raise Exception("Output grid not correct for: %s" % input_file)
    else:
        print("NOT CHECKING OUTPUT GRID for REGIONAL DATA")


def _cdoWrapper(operation, input_files, output_file, options=None):
    """
    Constructs a CDO command and runs it.

        $ cdo [<options>] <operation> <input_files> <output_file>

    """
    opts_string = ""
    if options is not None:
        opts_string = " ".join(options)

    if type(input_files) == str:
        input_files = [input_files]

    input_files_string = " ".join(input_files)

    cmd = "%s %s %s %s %s" % (cdo_path, opts_string, operation, input_files_string, output_file)
    print ("Running CDO command: %s" % cmd)

    start_time = time.time()

    # Set required Environment Variables for CDO
    os.environ["CDO_PCTL_NBINS"] = "1001"

    # Run the process
    proc = subprocess.Popen(shlex.split(cmd),
                            stderr=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            env=os.environ)

    # Get the return values
    retvals = proc.communicate()

    end_time = time.time()

    # Define a dictionary of outputs
    output = {"stdout": retvals[0],
              "stderr": retvals[1],
              "returncode": proc.returncode}

    print("CDO Outputs: stdout='{}'; stderr='{}'; return code='{}'".format(
        output["stdout"],
        output["stderr"],
        output["returncode"]))

    return_code = output["returncode"]
    return output


def _mapToDRS(file_path):
    """
    Maps a file to a MockDRS object - which is returned.
    """
    mdrs = MockDRS(file_path)
    return mdrs


def _getGridCellAreaVariable(var_id, path):
    """
    Looks in the file ``path`` to find the file that contains
    the grid cell areas.

    Returns None if cannot find file.
    """
    print "PATH:", path
    f = cdms.open(path)
    if var_id not in f.listvariables():
        raise Exception("Cannot find variable '%s' in file '%s'." % (var_id, path))

    v = f[var_id]
    f.close()

    try:
        acm = re.search("area:\s*(\w+)\s", v.cell_measures).groups()[0]
        acm_file_name = re.search("%s:\s*(%s_.+?\.nc)" % (acm, acm), v.associated_files).groups()[0]
    except Exception:
        print("Could not locate grid cell area file for '%s' in file '%s'." % (var_id, path))
        return None

    d = _mapToDRS(path)
    cell_areas_file = os.path.join(
        d.ARCHIVE_BASE, d.activity, d.product, d.institute,
        d.model, d.experiment, "fx", d.modeling_realm, "fx", "r0i0p0",
        "latest", acm, acm_file_name)

    if not os.path.isfile(cell_areas_file):
        print("Cell areas file not found at: %s" % cell_areas_file)
        return None

    return cell_areas_file
