import pytest
from rest_framework.settings import api_settings
# from rest_framework_json_api.settings import json_api_settings


def test_settings_invalid():
    with pytest.raises(AttributeError):
        a = api_settings.INVALID_SETTING


# def test_settings_default():
#     assert api_settings.UNIFORM_EXCEPTIONS is False


def test_settings_override(settings):
    settings.COMPACT_JSON = 'dasherize'
    assert settings.COMPACT_JSON == 'dasherize'
