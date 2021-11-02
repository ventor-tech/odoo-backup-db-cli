# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

# Stdlib:
import configparser

# Thirdparty:
from mock import patch
from odoo_backup_db_cli.protocols.sftp import SftpBackupHandler


@patch('odoo_backup_db_cli.protocols.sftp.pysftp')
@patch('odoo_backup_db_cli.protocols.sftp.SftpBackupHandler._delete_old_backups')
@patch('odoo_backup_db_cli.protocols.sftp.SftpBackupHandler._save_db')
@patch('odoo_backup_db_cli.protocols.sftp.SftpBackupHandler._save_filestore')
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
    sftp_backup_handler_instance = SftpBackupHandler(config, 'test')
    sftp_backup_handler_instance._connect()
    sftp_backup_handler_instance._save_db()
    sftp_backup_handler_instance._save_filestore()
    sftp_backup_handler_instance._delete_old_backups()
    sftp_backup_handler_instance._disconnect()
    save_filestore_mock.assert_called_once()
    save_db_mock.assert_called_once()
    delete_old_backups_mock.assert_called_once()
