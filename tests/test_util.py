import pytest

from regridder import util

from .common import CORDEX_NC, CMIP5_NC, ARCHIVE_BASE


def test_get_variable_name():
    assert util.get_variable_name(CORDEX_NC) == 'tasmin'
    assert util.get_variable_name(CMIP5_NC) == 'tas'


def test_convert_to_netcdf3():
    assert util.convert_to_netcdf3(CORDEX_NC, output_file='/tmp/test.nc') == '/tmp/test.nc'


def test_map_to_drs_cmip5():
    assert util.map_to_drs(CMIP5_NC, archive_base=ARCHIVE_BASE) is not None


@pytest.mark.skip(reason='not working')
def test_get_grid_cell_area_variable_cordex():
    assert util.get_grid_cell_area_variable(
        var_id='tasmin',
        path=CORDEX_NC,
        archive_base=ARCHIVE_BASE) is not None


def test_get_grid_cell_area_variable_cmip5():
    assert util.get_grid_cell_area_variable(
        var_id='tas',
        path=CMIP5_NC,
        archive_base=ARCHIVE_BASE) == \
        '/opt/data/cmip5/output1/MOHC/HadGEM2-ES/historical/fx/atmos/fx/r0i0p0/latest/areacella/areacella_fx_HadGEM2-ES_historical_r0i0p0.nc'  # noqa
