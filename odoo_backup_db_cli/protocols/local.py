# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


# Stdlib:
import os
import shutil
import tempfile
from datetime import datetime, timedelta

# Thirdparty:
from odoo_backup_db_cli.utils import CodeError

FORMAT_TIME = '%Y-%m-%d-%H-%M-%S'


def _local_save_db(config, environment, subfolder):
    path = os.path.join(config[environment].get('backup_location'), subfolder)
    mode = 0o755
    os.makedirs(path, mode=mode, exist_ok=True)
    db_path = os.path.join(path, 'dump.sql')
    os.rename('{0}/dump.sql'.format(tempfile.gettempdir()), db_path)
    return CodeError.SUCCESS


def _local_save_filestore(config, environment, subfolder):
    if config[environment].get('with_filestore') not in ('False', '0', None):
        path = os.path.join(config[environment].get('backup_location'), subfolder)
        filestore_path = os.path.join(path, 'filestore.zip')
        os.rename('{0}/filestore.zip'.format(tempfile.gettempdir()), filestore_path)
    return CodeError.SUCCESS


def _local_delete_old_backups(config, environment):  # noqa: C901, WPS231
    days = int(config[environment].get('clean_backup_after'))
    for root, dirs, _ in os.walk(config[environment].get('backup_location')):
        for dir in dirs:  # pragma: no cover - actually tested
            try:
                correct_dir = datetime.strptime(dir, FORMAT_TIME)
            except ValueError:
                continue
            if correct_dir + timedelta(days) < datetime.now():
                shutil.rmtree(os.path.abspath(os.path.join(root, dir)))
    return CodeError.SUCCESS


def _local_handler(config, environment):
    subfolder = datetime.now().strftime(FORMAT_TIME)
    _local_save_db(config, environment, subfolder)
    _local_save_filestore(config, environment, subfolder)
    _local_delete_old_backups(config, environment)
    return CodeError.SUCCESS
