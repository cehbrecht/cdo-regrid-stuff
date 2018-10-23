import os
import tempfile


from cdo import Cdo
cdo = Cdo()

from regridder import util

RESOURCE_DIR = os.path.dirname(os.path.abspath(os.path.join(__file__, '..')))

import logging
LOGGER = logging.getLogger('REGRIDDER')


def regrid(input_file, domain_type, output_base_dir='OUT', archive_base=None):
    # Define some rules regarding the inputs and how they map to information needed by this process
    if domain_type == "global":
        grid_definition_file = os.path.join(RESOURCE_DIR, 'grid_files', 'll1deg_grid.nc')
        # grid_short_name = "1-deg"
        output_dir = os.path.join(output_base_dir, "1_deg")
    else:
        regional_domain = os.path.basename(input_file).split("_")[1]
        grid_definition_file = os.path.join(RESOURCE_DIR, 'grid_files', 'll0.5deg_{}.nc'.format(regional_domain))
        # grid_short_name = "0.5-deg"
        output_dir = os.path.join(output_base_dir, "0.5_deg")

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    # Validate input grid first - check CDO can manage it
    validate_input_grid(input_file)

    # Determine output file name
    output_file = os.path.join(output_dir, os.path.basename(input_file))

    # We will need to select the main variable using the "select" operator piped into the CDO operator
    var_id = os.path.basename(input_file).split("_")[0]
    options = "-b F64"
    operation = '-select,name={}'.format(var_id)

    # Get the variable (in external file) that contains the grid cell area variable
    cell_areas_file = util.get_grid_cell_area_variable(var_id, input_file, archive_base=archive_base)
    if cell_areas_file:
        operation += " -setgridarea,{}".format(cell_areas_file)
    if domain_type == "global":
        operation = '-remapbil,{} {}'.format(grid_definition_file, operation)
        cdo.setgridtype('lonlat', input="{} {}".format(operation, input_file),
                        output=output_file, options=options)
    else:
        cdo.remapbil(grid_definition_file,
                     input="{} {}".format(operation, input_file),
                     output=output_file, options=options)

    validate_regridded_file(output_file, domain_type)

    if domain_type == "regional":
        util.convert_to_netcdf3(output_file)

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
        LOGGER.warn("NOT CHECKING OUTPUT GRID for REGIONAL DATA")
