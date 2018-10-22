from regridder.cdo_regridder import regrid


def test_regrid():
    paths = {"global": [
        "/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical/day/atmos/day/r1i1p1/v20120716/tas/tas_day_HadGEM2-ES_historical_r1i1p1_19791201-19891130.nc"  # noqa
        ],
        "regional":
        ["/Users/pingu/tmp/data/cordex/tasmin_AFR-44i_ECMWF-ERAINT_evaluation_r1i1p1_MOHC-HadRM3P_v1_mon_199001-199012.nc"]  # noqa
    }

    for domain_type, paths in paths.items():
        for path in paths:
            regrid(path, domain_type)
