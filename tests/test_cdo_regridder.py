from regridder.cdo_regridder import regrid

CMIP5_NC = "/opt/data/cmip5/tas_day_HadGEM2-ES_historical_r1i1p1_19791201-19891130.nc"
CORDEX_NC = "/opt/data/cordex/tasmin_AFR-44i_ECMWF-ERAINT_evaluation_r1i1p1_MOHC-HadRM3P_v1_mon_199001-199012.nc"


def test_regrid():
    regrid(CORDEX_NC, 'regional')
    # regrid(CMIP5_NC, 'global')
