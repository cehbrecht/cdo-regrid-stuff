from regridder import util

from .common import CORDEX_NC


def test_convert_to_netcdf3():
    assert util.convert_to_netcdf3(CORDEX_NC, output_file='/tmp/test.nc') == '/tmp/test.nc'
