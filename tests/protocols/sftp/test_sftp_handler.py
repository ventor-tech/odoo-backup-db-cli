# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

# Stdlib:
import configparser

# Thirdparty:
from mock import patch
from odoo_backup_db_cli.protocols.sftp import _sftp_handler
from odoo_backup_db_cli.utils import CodeError


@patch('odoo_backup_db_cli.protocols.sftp.pysftp')
@patch('odoo_backup_db_cli.protocols.sftp._sftp_delete_old_backups')
@patch('odoo_backup_db_cli.protocols.sftp._sftp_save_db')
@patch('odoo_backup_db_cli.protocols.sftp._sftp_save_filestore')
def test_ok(save_filestore_mock, save_db_mock, delete_old_backups_mock, pysftp_mock):
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
    res = _sftp_handler(config, 'test')
    save_filestore_mock.assert_called_once()
    save_db_mock.assert_called_once()
    delete_old_backups_mock.assert_called_once()
    assert res == CodeError.SUCCESS
