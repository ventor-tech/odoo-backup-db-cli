# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

# Stdlib:
import configparser
import os
import tempfile

# Thirdparty:
from odoo_backup_db_cli.protocols.local import _local_delete_old_backups
from odoo_backup_db_cli.utils import CodeError


def test_delete():
    path = '{0}/test_local_delete_old_backups/'.format(tempfile.gettempdir())
    test_folder = '2020-01-01-01-01-01'
    os.makedirs(os.path.dirname(path + test_folder), exist_ok=True)
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
        'backup_location': path,
        'clean_backup_after': '12',
        'db_name': 'test',
        'with_filestore': 'True',
        'filestore_location': '/tmp/test',
    }
    res = _local_delete_old_backups(config, 'test')
    try:
        os.rmdir(path)
    except OSError:
        pass
    assert res == CodeError.SUCCESS


def test_try_delete_incorrect():
    path = '{0}/test_local_delete_old_backups/'.format(tempfile.gettempdir())
    test_folder = '2020'
    os.makedirs(os.path.dirname(path + test_folder), exist_ok=True)
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
        'backup_location': path,
        'clean_backup_after': '12',
        'db_name': 'test',
        'with_filestore': 'True',
        'filestore_location': '/tmp/test',
    }
    res = _local_delete_old_backups(config, 'test')
    try:
        os.rmdir(path + test_folder)
        os.rmdir(path)
    except OSError:
        pass
    assert res == CodeError.SUCCESS


def test_not_delete():
    path = '{0}/test_local_delete_old_backups/'.format(tempfile.gettempdir())
    os.makedirs(os.path.dirname(path), exist_ok=True)
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
        'backup_location': path,
        'clean_backup_after': '12',
        'db_name': 'test',
        'with_filestore': 'True',
        'filestore_location': '/tmp/test',
    }
    res = _local_delete_old_backups(config, 'test')
    try:
        os.rmdir(path)
    except OSError:
        pass
    assert res == CodeError.SUCCESS
