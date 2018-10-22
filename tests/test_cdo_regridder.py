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
    assert regridder.map_to_drs(CORDEX_NC) == ''


def test_regrid():
    regridder.regrid(CORDEX_NC, 'regional')
    # regrid(CMIP5_NC, 'global')
