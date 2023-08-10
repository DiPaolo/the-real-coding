import json
from enum import Enum
from typing import List

from PySide6.QtCore import QSettings


class SettingsKey(Enum):
    WINDOW_GEOMETRY = 'windowGeometry'
    WINDOW_STATE = 'windowState'

    RECENT_CHOSEN_DIRS = 'recentChosenDirs'


def _get_settings():
    settings = QSettings()
    settings.setDefaultFormat(QSettings.Format.IniFormat)
    return settings


def get_settings_str_value(key: SettingsKey, default: str = ''):
    return _get_settings().value(key.value, default)


def set_settings_str_value(key: SettingsKey, value: str):
    _get_settings().setValue(key.value, value)


def get_settings_int_value(key: SettingsKey, default: int = 0):
    return _get_settings().value(key.value, default)


def set_settings_int_value(key: SettingsKey, value: int):
    _get_settings().setValue(key.value, value)


def get_settings_list_value(key: SettingsKey, default: List = None):
    if default is None:
        default = list()

    ret = _get_settings().value(key.value, '')
    if ret == '':
        return default

    return json.loads(ret)


def set_settings_list_value(key: SettingsKey, value: List):
    _get_settings().setValue(key.value, json.dumps(value))


def get_settings_byte_array_value(key: SettingsKey, default: bytes = None):
    return _get_settings().value(key.value, default)


def set_settings_byte_array_value(key: SettingsKey, value: str):
    _get_settings().setValue(key.value, value)
