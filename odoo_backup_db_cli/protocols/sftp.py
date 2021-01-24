# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


# Stdlib:
import os
import tempfile
from datetime import datetime, timedelta

# Thirdparty:
import pysftp
from odoo_backup_db_cli.utils import CodeError

FORMAT_TIME = '%Y-%m-%d-%H-%M-%S'


def _sftp_save_db(config, environment, sftp, subfolder):
    mode = 755
    sftp.makedirs(config[environment].get('backup_location'), mode)
    sftp.cwd(config[environment].get('backup_location'))
    previous_folder = sftp.pwd
    if subfolder not in sftp.listdir():
        sftp.mkdir(subfolder, mode=mode)
    sftp.cwd(subfolder)
    sftp.put('{0}/dump.sql'.format(tempfile.gettempdir()))
    os.remove('{0}/dump.sql'.format(tempfile.gettempdir()))
    sftp.cwd(previous_folder)
    return CodeError.SUCCESS


def _sftp_save_filestore(config, environment, sftp, subfolder):
    if config[environment].get('with_filestore') not in ('False', '0', None):
        previous_folder = sftp.pwd
        sftp.cwd(subfolder)
        sftp.put('{0}/filestore.zip'.format(tempfile.gettempdir()))
        os.remove('{0}/filestore.zip'.format(tempfile.gettempdir()))
        sftp.cwd(previous_folder)
    return CodeError.SUCCESS


def _sftp_delete_old_backups(config, environment, sftp):  # noqa: C901, WPS231
    days = int(config[environment].get('clean_backup_after'))
    for folder in sftp.listdir():  # pragma: no cover - actually tested
        try:
            correct_folder = datetime.strptime(folder, FORMAT_TIME)
        except ValueError:
            continue
        if correct_folder + timedelta(days) < datetime.now():
            for sftp_file in sftp.listdir(folder):
                previous_folder = sftp.pwd
                sftp.cwd(folder)
                sftp.remove(sftp_file)
                sftp.cwd(previous_folder)
            sftp.rmdir(folder)
    return CodeError.SUCCESS


def _sftp_handler(config, environment):
    with pysftp.Connection(
        config[environment].get('host'),
        port=int(config[environment].get('port')),
        username=config[environment].get('username'),
        password=config[environment].get('password'),
        private_key=config[environment].get('private_key'),
    ) as sftp:
        subfolder = datetime.now().strftime(FORMAT_TIME)
        _sftp_save_db(config, environment, sftp, subfolder)
        _sftp_save_filestore(config, environment, sftp, subfolder)
        _sftp_delete_old_backups(config, environment, sftp)
    return CodeError.SUCCESS
