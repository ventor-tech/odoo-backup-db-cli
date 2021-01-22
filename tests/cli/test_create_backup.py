# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

# Stdlib:
import configparser
import os
import tempfile

# Thirdparty:
from click.testing import CliRunner
from mock import patch
from odoo_backup_db_cli.cli import DEFAULT_ENVIRONMENT, importlib, main
from odoo_backup_db_cli.utils import CodeError


@patch.object(importlib, 'import_module')
@patch('odoo_backup_db_cli.cli.dump_filestore')
@patch('odoo_backup_db_cli.cli.dump_db')
def test_ok(dump_db_mock, dump_filestore_mock, import_module_mock):
    runner = CliRunner()
    path = '{0}/test_create_backup/test_ok.conf'.format(tempfile.gettempdir())
    config = configparser.ConfigParser()
    config['common'] = {}
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
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as configfile:
        config.write(configfile)
    res = runner.invoke(main, ('create-backup', 'test', '--path', path), None, None, False)
    dump_db_mock.assert_called_once()
    dump_filestore_mock.assert_called_once()
    import_module_mock.assert_called_once()
    os.remove(path)
    try:
        os.rmdir(path)
    except OSError:
        pass
    assert res.exit_code == CodeError.SUCCESS


def test_check_exist_config():
    runner = CliRunner()
    path = '{0}/test_create_backup/test_check_exist_config.conf'.format(tempfile.gettempdir())
    res = runner.invoke(main, ('create-backup', 'test', '--path', path))
    assert res.exit_code == CodeError.FILE_DOES_NOT_EXIST


def test_error_found():
    runner = CliRunner()
    path = '{0}/test_create_backup/test_error_found.conf'.format(tempfile.gettempdir())
    config = configparser.ConfigParser()
    config[DEFAULT_ENVIRONMENT] = {
        'db_host': 'localhost',
        'db_port': '5432',
        'db_username': 'odoo',
        'db_password': 'odoo',
    }
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as configfile:
        config.write(configfile)
    res = runner.invoke(main, ('create-backup', 'test', '--path', path), catch_exceptions=True)
    assert res.exit_code == CodeError.NO_SETTINGS
