# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

# Stdlib:
import configparser
import os
import tempfile

# Thirdparty:
from click.testing import CliRunner
from odoo_backup_db_cli.cli import DEFAULT_ENVIRONMENT, main
from odoo_backup_db_cli.utils import CodeError


def test_ok():
    runner = CliRunner()
    path = '{0}/test_update_config/test_ok.conf'.format(tempfile.gettempdir())
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
    parameters = (
        'update-config',
        '--path',
        path,
        '-e',
        'test',
        '-h',
        '0.0.0.0',
        '-p',
        '5434',
        '-u',
        'odoo2',
        '-w',
        '1234',
        '-t',
        'sftp',
        '-r',
        '5435',
        '-s',
        'True',
        '-U',
        'kek',
        '-W',
        'lol',
        '-K',
        '~/.ssh/id_rsa',
        '-b',
        '/tmp',
        '-c',
        '12',
        '-d',
        'test',
        '-F',
        '-f',
        '/tmp/test',
    )
    res = runner.invoke(main, parameters)
    config.read(path)
    os.remove(path)
    try:
        os.rmdir(os.path.dirname(path))
    except OSError:
        pass
    expected_config_common = {
        'db_host': 'localhost',
        'db_port': '5432',
        'db_username': 'odoo',
        'db_password': 'odoo',
    }
    expected_config_test = {
        'db_host': '0.0.0.0',
        'db_port': '5434',
        'db_username': 'odoo2',
        'db_password': '1234',
        'type': 'sftp',
        'port': '5435',
        'pasv': 'True',
        'username': 'kek',
        'password': 'lol',
        'private_key': '~/.ssh/id_rsa',
        'backup_location': '/tmp',
        'clean_backup_after': '12',
        'db_name': 'test',
        'with_filestore': 'True',
        'filestore_location': '/tmp/test',
    }
    assert res.exit_code == CodeError.SUCCESS
    assert config[DEFAULT_ENVIRONMENT] == expected_config_common
    assert config['test'] == expected_config_test


def test_check_exist_config():
    runner = CliRunner()
    path = '{0}/test_update_config/test_check_exist_config.conf'.format(tempfile.gettempdir())
    parameters = (
        'update-config',
        '--path',
        path,
        '-e',
        'test',
        '-h',
        '0.0.0.0',
        '-p',
        '5434',
        '-u',
        'odoo2',
        '-w',
        '1234',
        '-t',
        'sftp',
        '-H',
        '0.1.2.3',
        '-r',
        '5435',
        '-s',
        'True',
        '-U',
        'kek',
        '-W',
        'lol',
        '-K',
        '~/.ssh/id_rsa',
        '-b',
        '/tmp',
        '-c',
        '12',
        '-d',
        'test',
        '-F',
        '-f',
        '/tmp/test',
    )
    res = runner.invoke(main, parameters)
    assert res.exit_code == CodeError.FILE_DOES_NOT_EXIST
