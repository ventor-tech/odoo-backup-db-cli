# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


# Stdlib:
import os
import shutil

# Thirdparty:
from odoo_backup_db_cli.protocols.common import FSBackupHandler
from odoo_backup_db_cli.utils import CodeError


class LocalBackupHandler(FSBackupHandler):
    """Local Backup Handler."""

    def _save_db(self):
        path = os.path.join(self.backup_location, self.subfolder)
        mode = 0o755
        os.makedirs(path, mode=mode, exist_ok=True)
        db_path = os.path.join(path, 'dump.sql.gz')
        os.rename(self.tmp_dump, db_path)
        return CodeError.SUCCESS

    def _save_filestore(self):
        if self.with_filestore:
            path = os.path.join(self.backup_location, self.subfolder)
            filestore_path = os.path.join(path, 'filestore.zip')
            os.rename(self.tmp_zip, filestore_path)
        return CodeError.SUCCESS


    def _delete_old_backups(self):  # noqa: C901, WPS231
        for root, dirs, _ in os.walk(self.backup_location):
            for dir in dirs:  # pragma: no cover - actually tested
                if self._is_folder_to_remove(dir):
                    shutil.rmtree(os.path.abspath(os.path.join(root, dir)))
        return CodeError.SUCCESS
