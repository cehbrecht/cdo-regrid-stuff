import pytest

from regridder import cdo_regridder as regridder

CMIP5_NC = "/opt/data/cmip5/output1/MOHC/HadGEM2-ES/historical/day/atmos/day/r1i1p1/v20120716/tas/tas_day_HadGEM2-ES_historical_r1i1p1_19791201-19891130.nc"  # noqa
CORDEX_NC = "/opt/data/cordex/tasmin_AFR-44i_ECMWF-ERAINT_evaluation_r1i1p1_MOHC-HadRM3P_v1_mon_199001-199012.nc"


def test_validate_input_grid():
    regridder.validate_input_grid(CORDEX_NC)


def test_validate_regridded_file():
    regridder.validate_regridded_file(CORDEX_NC, 'regional')
    # regridder.validate_regridded_file(CMIP5_NC, 'global')


@pytest.mark.skip(reason='not working')
def test_map_to_drs():
    assert regridder.map_to_drs(CORDEX_NC) is not None


@pytest.mark.skip(reason='not working')
def test_get_grid_cell_area_variable():
    assert regridder.get_grid_cell_area_variable(var_id='tasmin', path=CORDEX_NC) is not None


def test_regrid_cordex():
    assert regridder.regrid(CORDEX_NC, 'regional') == \
        'OUT/0.5_deg/tasmin_AFR-44i_ECMWF-ERAINT_evaluation_r1i1p1_MOHC-HadRM3P_v1_mon_199001-199012.nc'


@pytest.mark.skip(reason='not working')
def test_regrid_cmip5():
    assert regridder.regrid(CMIP5_NC, 'global') == ''
