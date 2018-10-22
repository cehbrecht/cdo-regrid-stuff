from regridder.cdo_regridder import regrid


def test_regrid():
    paths = {
        "global": [
            "/opt/data/cmip5/tas_day_HadGEM2-ES_historical_r1i1p1_19791201-19891130.nc"
        ],
        "regional": [
            "/opt/data/cordex/tasmin_AFR-44i_ECMWF-ERAINT_evaluation_r1i1p1_MOHC-HadRM3P_v1_mon_199001-199012.nc"
        ]
    }

    for domain_type, paths in paths.items():
        for path in paths:
            regrid(path, domain_type)
