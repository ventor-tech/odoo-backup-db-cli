# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

# Stdlib:
import configparser

# Thirdparty:
from mock import patch
from odoo_backup_db_cli.protocols.local import _local_save_db, os
from odoo_backup_db_cli.utils import CodeError


@patch.object(os, 'makedirs')
@patch.object(os, 'rename')
def test_ok(rename_mock, makedirs_mock):
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
    res = _local_save_db(config, 'test', 'test')
    rename_mock.assert_called_once()
    makedirs_mock.assert_called_once()
    assert res == CodeError.SUCCESS
