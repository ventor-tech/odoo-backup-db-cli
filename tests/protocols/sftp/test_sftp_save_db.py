# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

# Stdlib:
import configparser

# Thirdparty:
from mock import patch
from odoo_backup_db_cli.protocols.sftp import SftpBackupHandler, pysftp, os


@patch.object(os, 'remove')
@patch.object(pysftp.Connection, 'makedirs')
@patch.object(pysftp.Connection, 'mkdir')
@patch.object(pysftp.Connection, 'listdir')
@patch('odoo_backup_db_cli.protocols.sftp.pysftp.Connection.pwd')
@patch.object(pysftp.Connection, 'put')
@patch.object(pysftp.Connection, 'cwd')
def test_ok_without_subfolder(
    cwd_mock,
    put_mock,
    pwd_mock,
    listdir_mock,
    mkdir_mock,
    makedirs_mock,
    remove_mock,
    ):
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
    listdir_mock.return_value = [""]
    sftp_backup_handler_instance = SftpBackupHandler(config, 'test')
    sftp_backup_handler_instance._save_db()
    assert cwd_mock.call_count == 3
    put_mock.assert_called_once()
    listdir_mock.assert_called_once()
    mkdir_mock.assert_called_once()
    makedirs_mock.assert_called_once()
    remove_mock.assert_called_once()


@patch.object(os, 'remove')
@patch.object(pysftp.Connection, 'makedirs')
@patch.object(pysftp.Connection, 'mkdir')
@patch.object(pysftp.Connection, 'listdir')
@patch('odoo_backup_db_cli.protocols.sftp.pysftp.Connection.pwd')
@patch.object(pysftp.Connection, 'put')
@patch.object(pysftp.Connection, 'cwd')
def test_ok_with_subfolder(
    cwd_mock,
    put_mock,
    pwd_mock,
    listdir_mock,
    mkdir_mock,
    makedirs_mock,
    remove_mock,
    ):
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
    listdir_mock.return_value = ["test"]
    sftp_backup_handler_instance = SftpBackupHandler(config, 'test')
    sftp_backup_handler_instance._save_db()
    assert cwd_mock.call_count == 3
    put_mock.assert_called_once()
    listdir_mock.assert_called_once()
    makedirs_mock.assert_called_once()
    mkdir_mock.assert_not_called()
    remove_mock.assert_called_once()
