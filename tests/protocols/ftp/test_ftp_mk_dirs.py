# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

# Stdlib:
import configparser
import tempfile

# Thirdparty:
from mock import call, patch
from odoo_backup_db_cli.protocols.ftp import FtpBackupHandler, ftplib


def cwd_result_generator():
    raise ftplib.Error
    yield 0


gen = cwd_result_generator()


def sideeffect(test):
    global gen
    for x in gen:
        return x


@patch.object(ftplib.FTP, 'cwd', side_effect=sideeffect)
@patch.object(ftplib.FTP, 'mkd')
@patch.object(ftplib.FTP, 'sendcmd')
def test_ok(sendcmd_mock, mkd_mock, cmd_mock):
    path = '{0}/test_ftp_mk_dirs'.format(tempfile.gettempdir())
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
    ftp_backup_handler_instance = FtpBackupHandler(config, 'test')
    ftp_backup_handler_instance._ftp_mk_dirs(path)
    sendcmd_mock.assert_called_once()
    mkd_mock.assert_called_once()
    cmd_mock.assert_has_calls([call(path), call(tempfile.gettempdir())])


def test_empty():
    path = ''
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
    ftp_backup_handler_instance = FtpBackupHandler(config, 'test')
    ftp_backup_handler_instance._ftp_mk_dirs(path)
