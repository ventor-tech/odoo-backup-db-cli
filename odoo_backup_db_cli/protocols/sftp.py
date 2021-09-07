# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


# Stdlib:
import os

# Thirdparty:
import pysftp
from odoo_backup_db_cli.protocols.common import RemoteBackupHandler, FSBackupHandler


class SftpBackupHandler(RemoteBackupHandler, FSBackupHandler):

    def _get_required_settings(self):
        res = super(SftpBackupHandler, self)._get_required_settings()
        res.append(
            (
                ('username', 'host', 'port'),
                'The creditials for the sftp server is not fully configured.'
            )
        )
        return res

    def check_config(self):
        super(SftpBackupHandler, self).check_config()
        if self.env.get('private_key') and self.env.get('password'):
            raise Exception('Only one of (private_key, password) '
                            'must be present in settings environment.')

    def _connect(self):
        self.sftp = pysftp.Connection(
            self.env.get('host'),
            port=int(self.env.get('port')),
            username=self.env.get('username'),
            password=self.env.get('password'),
            private_key=self.env.get('private_key'),
        )

    def _disconnect(self):
        self.sftp.close()

    def _save_db(self):
        mode = 755
        self.sftp.makedirs(self.backup_location, mode)
        self.sftp.cwd(self.backup_location)
        previous_folder = self.sftp.pwd
        if self.subfolder not in self.sftp.listdir():
            self.sftp.mkdir(self.subfolder, mode=mode)
        self.sftp.cwd(self.subfolder)
        self.sftp.put(self.tmp_dump)
        os.remove(self.tmp_dump)
        self.sftp.cwd(previous_folder)

    def _save_filestore(self):
        if self.with_filestore:
            previous_folder = self.sftp.pwd
            self.sftp.cwd(self.subfolder)
            self.sftp.put(self.tmp_zip)
            os.remove(self.tmp_zip)
            self.sftp.cwd(previous_folder)

    def _delete_old_backups(self):  # noqa: C901, WPS231
        for folder in self.sftp.listdir():  # pragma: no cover - actually tested
            if self._is_folder_to_remove(folder):
                for sftp_file in self.sftp.listdir(folder):
                    previous_folder = self.sftp.pwd
                    self.sftp.cwd(folder)
                    self.sftp.remove(sftp_file)
                    self.sftp.cwd(previous_folder)
                self.sftp.rmdir(folder)
