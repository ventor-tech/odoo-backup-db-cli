# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import configparser
import os
import tempfile

from click.testing import CliRunner
from odoo_backup_db_cli.cli import DEFAULT_ENVIRONMENT, main
from odoo_backup_db_cli.utils import CodeError


def test_ok():
    runner = CliRunner()
    path = '{0}/test_generate_common_config/test_ok.conf'.format(tempfile.gettempdir())
    res = runner.invoke(main, ('generate-common-config', '--path', path))
    config = configparser.ConfigParser()
    config.read(path)
    os.remove(path)
    try:
        os.rmdir(path)
    except OSError:
        pass
    expected_config = {
        'db_host': 'localhost',
        'db_port': '5432',
        'db_username': 'odoo',
        'db_password': 'odoo',
    }
    assert res.exit_code == 0
    assert config[DEFAULT_ENVIRONMENT] == expected_config


def test_check_exist_config():
    runner = CliRunner()
    path = '{0}/test_generate_common_config/test_check_exist_config.conf'.format(
        tempfile.gettempdir()
    )
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
    res = runner.invoke(main, ('generate-common-config', '--path', path))
    assert res.exit_code == CodeError.FILE_ALREADY_EXIST


def test_check_access():
    runner = CliRunner()
    path = '{0}/test_generate_common_config/test_check_access.conf'.format(tempfile.gettempdir())
    dir_path = '{0}/test_generate_common_config/'.format(tempfile.gettempdir())
    os.makedirs(dir_path, exist_ok=True)
    os.chmod(dir_path, 0o555)
    res = runner.invoke(main, ('generate-common-config', '--path', path))
    os.chmod(dir_path, 0o777)
    try:
        os.rmdir(dir_path)
    except OSError:
        pass
    assert res.exit_code == CodeError.ACCESS_ERROR
