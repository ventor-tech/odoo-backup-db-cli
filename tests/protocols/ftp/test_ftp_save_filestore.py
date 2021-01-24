# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

# Stdlib:
import configparser

# Thirdparty:
from mock import patch
from odoo_backup_db_cli.protocols.ftp import _ftp_save_filestore, ftplib, os
from odoo_backup_db_cli.utils import CodeError


@patch.object(os, 'remove')
@patch.object(ftplib.FTP, 'pwd')
@patch.object(ftplib.FTP, 'storbinary')
@patch.object(ftplib.FTP, 'cwd')
@patch('odoo_backup_db_cli.protocols.ftp.open')
def test_with_filestore(
    open_mock,
    cwd_mock,
    storbinary_mock,
    pwd_mock,
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
    res = _ftp_save_filestore(config, 'test', ftplib.FTP, 'test')
    open_mock.assert_called_once()
    assert cwd_mock.call_count == 2
    storbinary_mock.assert_called_once()
    pwd_mock.assert_called_once()
    remove_mock.assert_called_once()
    assert res == CodeError.SUCCESS


@patch.object(os, 'remove')
@patch.object(ftplib.FTP, 'pwd')
@patch.object(ftplib.FTP, 'storbinary')
@patch.object(ftplib.FTP, 'cwd')
@patch('odoo_backup_db_cli.protocols.ftp.open')
def test_without_filestore(
    open_mock,
    cwd_mock,
    storbinary_mock,
    pwd_mock,
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
        'with_filestore': 'False',
        'filestore_location': '/tmp/test',
    }
    res = _ftp_save_filestore(config, 'test', ftplib.FTP, 'test')
    open_mock.assert_not_called()
    cwd_mock.assert_not_called()
    storbinary_mock.assert_not_called()
    pwd_mock.assert_not_called()
    remove_mock.assert_not_called()
    assert res == CodeError.SUCCESS
