import pytest

from regridder.mock_drs import MockDRS

from .common import CMIP5_NC, ARCHIVE_BASE

FX_NC = "/cmip5/output1/MPI-M/MPI-ESM-P/piControl/fx/atmos/fx/r0i0p0/latest/orog/orog_fx_MPI-ESM-P_piControl_r0i0p0.nc"


def test_mock_drs_cmip5():
    m = MockDRS(CMIP5_NC, archive_base=ARCHIVE_BASE)
    for i in m.asIter():
        print(i)
    m2 = MockDRS(CMIP5_NC, archive_base=ARCHIVE_BASE)
    print(m2.asDict())


@pytest.mark.skip(reason='can not handle fx')
def test_mock_drs_fx():
    MockDRS(FX_NC)
