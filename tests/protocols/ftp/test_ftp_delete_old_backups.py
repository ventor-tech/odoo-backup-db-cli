# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

# Stdlib:
import configparser

# Thirdparty:
from mock import patch
from odoo_backup_db_cli.protocols.ftp import FtpBackupHandler, ftplib


@patch.object(ftplib.FTP, 'nlst', side_effect=(('2020-01-01-01-01-01',),('1', '2')))
@patch.object(ftplib.FTP, 'rmd')
@patch.object(ftplib.FTP, 'delete')
def test_delete(
    delete_mock,
    rmd_mock,
    nlst_mock,
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
        'backup_location': "/tmp",
        'clean_backup_after': '12',
        'db_name': 'test',
        'with_filestore': 'True',
        'filestore_location': '/tmp/test',
    }
    ftp_backup_handler_instance = FtpBackupHandler(config, 'test')
    ftp_backup_handler_instance._ftp_delete_old_backups()
    assert delete_mock.call_count == 2
    assert nlst_mock.call_count == 2
    rmd_mock.assert_called_once()


@patch.object(ftplib.FTP, 'nlst', side_effect=(('2020',),('1', '2')))
@patch.object(ftplib.FTP, 'rmd')
@patch.object(ftplib.FTP, 'delete')
def test_try_delete_incorrect(
    delete_mock,
    rmd_mock,
    nlst_mock,
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
        'backup_location': "/tmp",
        'clean_backup_after': '12',
        'db_name': 'test',
        'with_filestore': 'True',
        'filestore_location': '/tmp/test',
    }
    ftp_backup_handler_instance = FtpBackupHandler(config, 'test')
    ftp_backup_handler_instance._ftp_delete_old_backups()
    assert delete_mock.call_count == 0
    assert nlst_mock.call_count == 1
    rmd_mock.assert_not_called()


@patch.object(ftplib.FTP, 'nlst', side_effect=((),('1', '2')))
@patch.object(ftplib.FTP, 'rmd')
@patch.object(ftplib.FTP, 'delete')
def test_not_delete(
    delete_mock,
    rmd_mock,
    nlst_mock,
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
        'backup_location': "/tmp",
        'clean_backup_after': '12',
        'db_name': 'test',
        'with_filestore': 'True',
        'filestore_location': '/tmp/test',
    }
    ftp_backup_handler_instance = FtpBackupHandler(config, 'test')
    ftp_backup_handler_instance._ftp_delete_old_backups()
    delete_mock.assert_not_called()
    nlst_mock.assert_called_once()
    rmd_mock.assert_not_called()
