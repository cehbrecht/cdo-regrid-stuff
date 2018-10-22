from regridder import cdo_regridder as regridder

CMIP5_NC = "/opt/data/cmip5/tas_day_HadGEM2-ES_historical_r1i1p1_19791201-19891130.nc"
CORDEX_NC = "/opt/data/cordex/tasmin_AFR-44i_ECMWF-ERAINT_evaluation_r1i1p1_MOHC-HadRM3P_v1_mon_199001-199012.nc"


def test_validate_input_grid():
    regridder.validate_input_grid(CORDEX_NC)


def test_regrid():
    regridder.regrid(CORDEX_NC, 'regional')
    # regrid(CMIP5_NC, 'global')
