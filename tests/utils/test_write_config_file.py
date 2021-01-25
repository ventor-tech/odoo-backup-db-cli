# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

# Stdlib:
import configparser
import os
import tempfile

# Thirdparty:
from odoo_backup_db_cli.utils import CodeError, write_config_file


def test_ok():
    path = '{0}/test_write_config_file/test_ok.conf'.format(tempfile.gettempdir())
    config = configparser.ConfigParser()
    config['common'] = {
        'db_host': '0.0.0.0',
        'db_port': '5434',
        'db_username': 'odoo2',
        'db_password': '1234',
    }
    os.makedirs(os.path.dirname(path), exist_ok=True)
    res = write_config_file(config, path)
    os.remove(path)
    try:
        os.rmdir(os.path.dirname(path))
    except OSError:
        pass
    assert res == CodeError.SUCCESS


def test_check_access_file():
    path = '{0}/test_write_config_file/test_check_access_file.conf'.format(tempfile.gettempdir())
    dir_path = '{0}/test_write_config_file/'.format(tempfile.gettempdir())
    os.makedirs(dir_path, exist_ok=True)
    os.chmod(dir_path, 0o555)
    config = configparser.ConfigParser()
    config['common'] = {
        'db_host': '0.0.0.0',
        'db_port': '5434',
        'db_username': 'odoo2',
        'db_password': '1234',
    }
    res = write_config_file(config, path)
    os.chmod(dir_path, 0o777)
    try:
        os.rmdir(dir_path)
    except OSError:
        pass
    assert res == CodeError.ACCESS_FILE_ERROR
