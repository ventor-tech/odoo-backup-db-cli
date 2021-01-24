# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

# Stdlib:
import configparser

# Thirdparty:
from mock import patch
from odoo_backup_db_cli.protocols.local import _local_save_filestore, os
from odoo_backup_db_cli.utils import CodeError


@patch.object(os, 'rename')
def test_with_filestore(rename_mock):
    config = configparser.ConfigParser()
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
    res = _local_save_filestore(config, 'test', 'test')
    rename_mock.assert_called_once()
    assert res == CodeError.SUCCESS

@patch.object(os, 'rename')
def test_without_filestore(rename_mock):
    config = configparser.ConfigParser()
    config['test'] = {
        'with_filestore': 'False',
        'filestore_location': '/tmp/test',
    }
    res = _local_save_filestore(config, 'test', 'test')
    rename_mock.assert_not_called()
    assert res == CodeError.SUCCESS
