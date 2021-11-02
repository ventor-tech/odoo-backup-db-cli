# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

# Stdlib:
import configparser

# Thirdparty:
from odoo_backup_db_cli.protocols.ftp import FtpBackupHandler
from odoo_backup_db_cli.protocols.local import LocalBackupHandler
from odoo_backup_db_cli.protocols.sftp import SftpBackupHandler
from odoo_backup_db_cli.utils import CodeError


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
        # 'type': 'local',
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
        'with_db': 'True',
        'filestore_location': '/tmp/test',
    }
    return config


def test_env():
    config = get_test_config()
    backup_instance = LocalBackupHandler(config, 'test2')
    try:
        backup_instance.check_config()
    except Exception:
        pass  # noqa: WPS420
        # Do nothing
    assert backup_instance.code_error == CodeError.NO_SETTINGS


def test_backup_location():
    config = get_test_config()
    del config['test']['backup_location']
    backup_instance = LocalBackupHandler(config, 'test')
    try:
        backup_instance.check_config()
    except Exception:
        pass  # noqa: WPS420
        # Do nothing
    assert backup_instance.code_error == CodeError.NO_SETTINGS


def test_clean_backup_after():
    config = get_test_config()
    del config['test']['clean_backup_after']
    backup_instance = LocalBackupHandler(config, 'test')
    try:
        backup_instance.check_config()
    except Exception:
        pass  # noqa: WPS420
        # Do nothing
    assert backup_instance.code_error == CodeError.NO_SETTINGS


def test_clean_backup_after_is_integer():
    config = get_test_config()
    config['test']['clean_backup_after'] = '1'
    backup_instance = LocalBackupHandler(config, 'test')
    try:
        backup_instance.check_config()
    except Exception:
        pass  # noqa: WPS420
        # Do nothing
    assert backup_instance.code_error == CodeError.SUCCESS


def test_with_filestore():
    config = get_test_config()
    del config['test']['with_filestore']
    backup_instance = LocalBackupHandler(config, 'test')
    try:
        backup_instance.check_config()
    except Exception:
        pass  # noqa: WPS420
        # Do nothing
    assert backup_instance.code_error == CodeError.SUCCESS


def test_filestore_location():
    config = get_test_config()
    del config['test']['filestore_location']
    backup_instance = LocalBackupHandler(config, 'test')
    try:
        backup_instance.check_config()
    except Exception:
        pass  # noqa: WPS420
        # Do nothing
    assert backup_instance.code_error == CodeError.NO_SETTINGS


def test_all_config_fields():
    config = get_test_config()
    del config['test']['db_username']
    del config['common']['db_username']
    backup_instance = LocalBackupHandler(config, 'test')
    try:
        backup_instance.check_config()
    except Exception:
        pass  # noqa: WPS420
        # Do nothing
    assert backup_instance.code_error == CodeError.NO_SETTINGS


def test_types_ftp():
    config = get_test_config()
    del config['test']['pasv']
    backup_instance = FtpBackupHandler(config, 'test')
    try:
        backup_instance.check_config()
    except Exception:
        pass  # noqa: WPS420
        # Do nothing
    assert backup_instance.code_error == CodeError.NO_SETTINGS


def test_types_sftp_ok():
    config = get_test_config()
    config['test']['type'] = 'sftp'
    del config['test']['private_key']
    backup_instance = SftpBackupHandler(config, 'test')
    try:
        backup_instance.check_config()
    except Exception:
        pass  # noqa: WPS420
        # Do nothing
    assert backup_instance.code_error == CodeError.SUCCESS


def test_types_sftp_full():
    config = get_test_config()
    backup_instance = SftpBackupHandler(config, 'test')
    try:
        backup_instance.check_config()
    except Exception:
        pass  # noqa: WPS420
        # Do nothing
    assert backup_instance.code_error == CodeError.INVALID_SETTINGS


def test_types_sftp_not_private_key_and_pasv():
    config = get_test_config()
    config['test']['type'] = 'sftp'
    del config['test']['private_key']
    del config['test']['pasv']
    backup_instance = SftpBackupHandler(config, 'test')
    try:
        backup_instance.check_config()
    except Exception:
        pass  # noqa: WPS420
        # Do nothing
    assert backup_instance.code_error == CodeError.NO_SETTINGS


def test_types_sftp_not_private_key_and_password():
    config = get_test_config()
    config['test']['type'] = 'sftp'
    del config['test']['private_key']
    del config['test']['password']
    backup_instance = SftpBackupHandler(config, 'test')
    try:
        backup_instance.check_config()
    except Exception:
        pass  # noqa: WPS420
        # Do nothing
    assert backup_instance.code_error == CodeError.NO_SETTINGS
