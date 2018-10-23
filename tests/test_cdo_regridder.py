import pytest

from regridder import cdo_regridder as regridder

from .common import CMIP5_NC, CORDEX_NC, ARCHIVE_BASE


def test_create_output_dir():
    assert regridder.create_output_dir('/tmp/out', domain_type='global') == '/tmp/out/1_deg'
    assert regridder.create_output_dir('/tmp/out', domain_type='regional') == '/tmp/out/0.5_deg'


def test_get_grid_definition_file():
    assert 'grid_files/ll1deg_grid.nc' in regridder.get_grid_definition_file(CMIP5_NC, domain_type='global')
    assert 'grid_files/ll0.5deg_AFR-44i.nc' in regridder.get_grid_definition_file(CORDEX_NC, domain_type='regional')


def test_validate_input_grid():
    regridder.validate_input_grid(CORDEX_NC)


def test_validate_regridded_file_coredex():
    regridder.validate_regridded_file(CORDEX_NC, 'regional')


@pytest.mark.skip(reason='not working')
def test_validate_regridded_file_cmip5():
    regridder.validate_regridded_file(CMIP5_NC, 'global')


def test_regrid_cordex():
    assert regridder.regrid(CORDEX_NC, 'regional', archive_base=ARCHIVE_BASE) == \
        'OUT/0.5_deg/tasmin_AFR-44i_ECMWF-ERAINT_evaluation_r1i1p1_MOHC-HadRM3P_v1_mon_199001-199012.nc'


@pytest.mark.skip(reason='not working')
def test_regrid_cmip5():
    assert regridder.regrid(CMIP5_NC, 'global', archive_base=ARCHIVE_BASE) == ''
