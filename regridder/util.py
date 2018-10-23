import shutil

from nco import Nco
nco = Nco()

import logging
LOGGER = logging.getLogger('REGRIDDER')


def convert_to_netcdf3(filename, output_file=None):
    output_file = output_file or filename
    tmp_file = filename[:-3] + "-tmp.nc"
    nco.ncks(input=filename, output=tmp_file, options=['-3'])
    shutil.move(tmp_file, output_file)
    LOGGER.info("Converted to NetCDF3 file: {}".format(output_file))
    return output_file
