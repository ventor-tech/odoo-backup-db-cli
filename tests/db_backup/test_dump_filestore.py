# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

# Stdlib:
import configparser

# Thirdparty:
from mock import patch
from odoo_backup_db_cli.db_backup import dump_filestore, shutil
from odoo_backup_db_cli.utils import CodeError


@patch.object(shutil, 'make_archive')
def test_with_filestore(make_archive_mock):
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
    res = dump_filestore(config, 'test')
    make_archive_mock.assert_called_once()
    assert res == CodeError.SUCCESS


@patch.object(shutil, 'make_archive')
def test_filestore_false(make_archive_mock):
    config = configparser.ConfigParser()
    config['test'] = {
        'db_name': 'test',
        'with_filestore': 'False',
        'filestore_location': '/tmp/test',
    }
    res = dump_filestore(config, 'test')
    make_archive_mock.assert_not_called()
    assert res == CodeError.SUCCESS
