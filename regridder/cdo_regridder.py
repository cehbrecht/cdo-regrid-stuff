# Standard library imports
import time
import re
import os
import shutil
import shlex
import tempfile

from cdo import Cdo
cdo = Cdo()

from nco import Nco
nco = Nco()

from regridder.mock_drs import MockDRS
import cdms2 as cdms

import logging
LOGGER = logging.getLogger('REGRIDDER')


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
    validate_input_grid(input_file)

    # Determine output file name
    output_file_name = os.path.split(input_file)[1]
    output_file = os.path.join(output_dir, output_file_name)

    # We will need to select the main variable using the "select" operator piped into the CDO operator
    var_id = os.path.basename(input_file).split("_")[0]
    options = "-b F64"

    # Get the variable (in external file) that contains the grid cell area variable
    cell_areas_file = _getGridCellAreaVariable(var_id, input_file)

    if cell_areas_file:
        # operation += " -setgridarea,%s" % cell_areas_file
        cdo.setgridarea(cell_areas_file, input=input_file, output='/tmp/out_gridarea.nc')
        input_file = '/tmp/out_gridarea.nc'
    cdo.select('name={}'.format(var_id), input=input_file, output='/tmp/out_select.nc', options=options)
    if domain_type == "global":
        cdo.remapbil(grid_definition_file, input='/tmp/out_select.nc', output='/tmp/out_remap.nc', options=options)
        cdo.setgridtype(input='/tmp/out_remap.nc', output=output_file, options=options)
    else:
        cdo.remapbil(grid_definition_file, input='/tmp/out_select.nc', output=output_file, options=options)

    validate_regridded_file(output_file, domain_type)

    if domain_type == "regional":
        # Convert to NetCDF 3
        tmp_file = output_file[:-3] + "-tmp.nc"
        nco.ncks(input=output_file, output=tmp_file, options=['-3'])
        shutil.move(tmp_file, output_file)
        print("Converted to NetCDF3 file: %s" % output_file)

    return output_file


def validate_input_grid(input_file):
    _, tmp_file = tempfile.mkstemp()
    cdo.timmean(input="-seltimestep,1 {}".format(input_file), output=tmp_file)

    # Analyse the output for the error "generic" meaning that cdo does not recognise the grid which may mean
    # that the file contains no fields, just a time series
    # if outputs["stderr"].replace("\n", "").find("generic") > -1:
    #    raise Exception(
    #        "No spatial grid in this dataset or not recognised grid. Please check the grid in the dataset.")


def validate_regridded_file(input_file, domain_type):
    sinfo = cdo.sinfo(input=input_file)

    if domain_type == "global":
        if "points=64800 (360x180)" not in sinfo:
            raise Exception("Output grid not correct for: {}".format(input_file))
    else:
        print("NOT CHECKING OUTPUT GRID for REGIONAL DATA")


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
    LOGGER.debug("Path: {}".format(path))
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
