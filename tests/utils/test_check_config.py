# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

# Stdlib:
import configparser

# Thirdparty:
from odoo_backup_db_cli.utils import CodeError, check_config


def get_test_config():
    config = configparser.ConfigParser()
    config['common'] = {
        'db_host': '0.0.0.0',
        'db_port': '5434',
        'db_username': 'odoo2',
        'db_password': '1234',
    }
    config['test'] = {
        'db_host': '0.0.0.0',
        'db_port': '5434',
        'db_username': 'odoo2',
        'db_password': '1234',
        'type': 'local',
        'host': '0.1.2.3',
        'port': '5435',
        'pasv': 'True',
        'username': 'kek',
        'password': 'lol',
        'private_key': '~/.ssh/id_rsa',
        'backup_location': '/tmp/test',
        'clean_backup_after': '12',
        'db_name': 'test',
        'with_filestore': 'True',
        'filestore_location': '/tmp/test',
    }
    return config


def test_env():
    config = get_test_config()
    res = check_config(config, 'test2')
    assert res == CodeError.NO_SETTINGS


def test_backup_location():
    config = get_test_config()
    del config['test']['backup_location']
    res = check_config(config, 'test')
    assert res == CodeError.NO_SETTINGS


def test_clean_backup_after():
    config = get_test_config()
    del config['test']['clean_backup_after']
    res = check_config(config, 'test')
    assert res == CodeError.NO_SETTINGS


def test_clean_backup_after_is_integer():
    config = get_test_config()
    config['test']['clean_backup_after'] = "1.1"
    res = check_config(config, 'test')
    assert res == CodeError.INVALID_SETTINGS


def test_with_filestore():
    config = get_test_config()
    del config['test']['with_filestore']
    res = check_config(config, 'test')
    assert res == CodeError.SUCCESS


def test_filestore_location():
    config = get_test_config()
    del config['test']['filestore_location']
    res = check_config(config, 'test')
    assert res == CodeError.NO_SETTINGS


def test_all_config_fields():
    config = get_test_config()
    del config['test']['db_username']
    del config['common']['db_username']
    res = check_config(config, 'test')
    assert res == CodeError.NO_SETTINGS


def test_types_another():
    config = get_test_config()
    config['test']['type'] = 'test'
    res = check_config(config, 'test')
    assert res == CodeError.NO_SETTINGS


def test_types_ftp_ok():
    config = get_test_config()
    config['test']['type'] = 'ftp'
    res = check_config(config, 'test')
    assert res == CodeError.SUCCESS


def test_types_ftp():
    config = get_test_config()
    config['test']['type'] = 'ftp'
    del config['test']['pasv']
    res = check_config(config, 'test')
    assert res == CodeError.NO_SETTINGS


def test_types_sftp_ok():
    config = get_test_config()
    config['test']['type'] = 'sftp'
    del config['test']['private_key']
    res = check_config(config, 'test')
    assert res == CodeError.SUCCESS


def test_types_sftp_full():
    config = get_test_config()
    config['test']['type'] = 'sftp'
    res = check_config(config, 'test')
    assert res == CodeError.INVALID_SETTINGS


def test_types_sftp_not_private_key_and_pasv():
    config = get_test_config()
    config['test']['type'] = 'sftp'
    del config['test']['private_key']
    del config['test']['pasv']
    res = check_config(config, 'test')
    assert res == CodeError.NO_SETTINGS


def test_types_sftp_not_private_key_and_password():
    config = get_test_config()
    config['test']['type'] = 'sftp'
    del config['test']['private_key']
    del config['test']['password']
    res = check_config(config, 'test')
    assert res == CodeError.NO_SETTINGS
