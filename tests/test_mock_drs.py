import pytest

from regridder.mock_drs import MockDRS

from .common import CMIP5_NC

FX_NC = "/cmip5/output1/MPI-M/MPI-ESM-P/piControl/fx/atmos/fx/r0i0p0/latest/orog/orog_fx_MPI-ESM-P_piControl_r0i0p0.nc"
TEST_NC = "/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/v20120928/ta/ta_Amon_HadGEM2-ES_rcp85_r1i1p1_200512-203011.nc"  # noqa


def test_mock_drs_cmip5():
    m = MockDRS(TEST_NC)
    for i in m.asIter():
        print(i)
    m2 = MockDRS(TEST_NC)
    print(m2.asDict())


def test_mock_drs_cmip5_archive_base():
    m2 = MockDRS(CMIP5_NC, archive_base='/opt/data')
    print(m2.asDict())


@pytest.mark.skip(reason='can not handle fx')
def test_mock_drs_fx():
    MockDRS(FX_NC)
