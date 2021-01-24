# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

# Stdlib:
import configparser

# Thirdparty:
from mock import patch
from odoo_backup_db_cli.protocols.sftp import _sftp_delete_old_backups, pysftp
from odoo_backup_db_cli.utils import CodeError

@patch('odoo_backup_db_cli.protocols.sftp.pysftp.Connection.pwd')
@patch.object(pysftp.Connection, 'listdir', side_effect=(('2020-01-01-01-01-01',),('1', '2')))
@patch.object(pysftp.Connection, 'cwd')
@patch.object(pysftp.Connection, 'rmdir')
@patch.object(pysftp.Connection, 'remove')
def test_delete(
    remove_mock,
    rmdir_mock,
    cwd_mock,
    listdir_mock,
    pwd_mock,
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
    res = _sftp_delete_old_backups(config, 'test', pysftp.Connection)
    assert remove_mock.call_count == 2
    assert listdir_mock.call_count == 2
    assert cwd_mock.call_count == 4
    rmdir_mock.assert_called_once()
    assert res == CodeError.SUCCESS


@patch('odoo_backup_db_cli.protocols.sftp.pysftp.Connection.pwd')
@patch.object(pysftp.Connection, 'listdir', side_effect=(('2020',),('1', '2')))
@patch.object(pysftp.Connection, 'cwd')
@patch.object(pysftp.Connection, 'rmdir')
@patch.object(pysftp.Connection, 'remove')
def test_try_delete_incorrect(
    remove_mock,
    rmdir_mock,
    cwd_mock,
    listdir_mock,
    pwd_mock,
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
    res = _sftp_delete_old_backups(config, 'test', pysftp.Connection)
    assert remove_mock.call_count == 0
    assert listdir_mock.call_count == 1
    assert cwd_mock.call_count == 0
    rmdir_mock.assert_not_called()
    assert res == CodeError.SUCCESS


@patch('odoo_backup_db_cli.protocols.sftp.pysftp.Connection.pwd')
@patch.object(pysftp.Connection, 'listdir', side_effect=((),('1', '2')))
@patch.object(pysftp.Connection, 'cwd')
@patch.object(pysftp.Connection, 'rmdir')
@patch.object(pysftp.Connection, 'remove')
def test_not_delete(
    remove_mock,
    rmdir_mock,
    cwd_mock,
    listdir_mock,
    pwd_mock,
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
    res = _sftp_delete_old_backups(config, 'test', pysftp.Connection)
    remove_mock.assert_not_called()
    listdir_mock.assert_called_once()
    rmdir_mock.assert_not_called()
    cwd_mock.assert_not_called()
    assert res == CodeError.SUCCESS
