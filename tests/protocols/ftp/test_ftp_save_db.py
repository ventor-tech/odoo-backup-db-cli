# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

# Stdlib:
import configparser

# Thirdparty:
from mock import patch
from odoo_backup_db_cli.protocols.ftp import FtpBackupHandler, ftplib, os


@patch.object(os, 'remove')
@patch.object(ftplib.FTP, 'mkd')
@patch.object(ftplib.FTP, 'nlst')
@patch.object(ftplib.FTP, 'pwd')
@patch.object(ftplib.FTP, 'storbinary')
@patch.object(ftplib.FTP, 'cwd')
@patch('odoo_backup_db_cli.protocols.ftp.open')
@patch('odoo_backup_db_cli.protocols.ftp.FtpBackupHandler._ftp_mk_dirs')
def test_ok_without_subfolder(
    ftp_mk_dirs_mock,
    open_mock,
    cwd_mock,
    storbinary_mock,
    pwd_mock,
    nlst_mock,
    mkd_mock,
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
    nlst_mock.return_value = [""]
    ftp_backup_handler_instance = FtpBackupHandler(config, 'test')
    ftp_backup_handler_instance._connect()
    ftp_backup_handler_instance._save_db()
    ftp_mk_dirs_mock.assert_called_once()
    open_mock.assert_called_once()
    assert cwd_mock.call_count == 2
    storbinary_mock.assert_called_once()
    pwd_mock.assert_called_once()
    nlst_mock.assert_called_once()
    mkd_mock.assert_called_once()
    remove_mock.assert_called_once()


@patch.object(os, 'remove')
@patch.object(ftplib.FTP, 'mkd')
@patch.object(ftplib.FTP, 'nlst')
@patch.object(ftplib.FTP, 'pwd')
@patch.object(ftplib.FTP, 'storbinary')
@patch.object(ftplib.FTP, 'cwd')
@patch('odoo_backup_db_cli.protocols.ftp.open')
@patch('odoo_backup_db_cli.protocols.ftp.FtpBackupHandler._ftp_mk_dirs')
def test_ok_with_subfolder(
    ftp_mk_dirs_mock,
    open_mock,
    cwd_mock,
    storbinary_mock,
    pwd_mock,
    nlst_mock,
    mkd_mock,
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
    nlst_mock.return_value = ["test"]
    ftp_backup_handler_instance = FtpBackupHandler(config, 'test')
    ftp_backup_handler_instance._connect()
    ftp_backup_handler_instance._save_db()
    ftp_mk_dirs_mock.assert_called_once()
    open_mock.assert_called_once()
    assert cwd_mock.call_count == 2
    storbinary_mock.assert_called_once()
    pwd_mock.assert_called_once()
    nlst_mock.assert_called_once()
    mkd_mock.assert_not_called()
    remove_mock.assert_called_once()
