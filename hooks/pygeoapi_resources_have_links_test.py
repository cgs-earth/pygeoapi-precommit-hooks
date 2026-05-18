

from pathlib import Path

from .pygeoapi_resources_have_links import valid_yaml_with_links


def test_valid_yaml_with_links():
    config = Path(__file__).parent / "testdata/wwdh-config.yml"
    assert valid_yaml_with_links(config.as_posix())

def test_valid_yaml_with_no_links_in_process():
    asu_config = Path(__file__).parent / "testdata/asu-config.yml"
    assert valid_yaml_with_links(asu_config.as_posix())

def test_invalid_yaml_with_links():
    config = Path(__file__).parent / "testdata/invalid-wwdh-config.yml"
    assert not valid_yaml_with_links(config.as_posix())