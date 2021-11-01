# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


# Stdlib:
import os

# Thirdparty:
import pysftp
from odoo_backup_db_cli.protocols.common import FSBackupHandler, RemoteBackupHandler
from odoo_backup_db_cli.utils import CodeError


class SftpBackupHandler(RemoteBackupHandler, FSBackupHandler):
    """SFTP Backup Handler."""

    def check_config(self):
        """Checks the config."""
        super().check_config()
        if self.env.get('private_key') and self.env.get('password'):
            self.code_error = CodeError.INVALID_SETTINGS
            raise Exception('Only one of (private_key, password) '
                            'must be present in settings environment.')

        if not self.env.get('private_key') and not self.env.get('password'):
            self.code_error = CodeError.NO_SETTINGS
            raise Exception('Private_key or Password '
                            'must be present in settings environment.')

    def _connect(self):
        self.sftp = pysftp.Connection(
            self.env.get('host'),
            port=int(self.env.get('port')),
            username=self.env.get('username'),
            password=self.env.get('password'),
            private_key=self.env.get('private_key'),
        )

    def _delete_old_backups(self):  # noqa: C901, WPS231
        for folder in self.sftp.listdir():  # pragma: no cover - actually tested
            if self._is_folder_to_remove(folder):
                for sftp_file in self.sftp.listdir(folder):
                    previous_folder = self.sftp.pwd
                    self.sftp.cwd(folder)
                    self.sftp.remove(sftp_file)
                    self.sftp.cwd(previous_folder)
                self.sftp.rmdir(folder)
        return CodeError.SUCCESS

    def _disconnect(self):
        self.sftp.close()

    def _get_required_settings(self):
        res = super()._get_required_settings()
        res.append(
            (
                ('username', 'host', 'port', 'pasv'),
                'The credentials for the ftp server is not fully configured.'
            )
        )
        return res

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
        return CodeError.SUCCESS

    def _save_filestore(self):
        if self.with_filestore:
            previous_folder = self.sftp.pwd
            self.sftp.cwd(self.subfolder)
            self.sftp.put(self.tmp_zip)
            os.remove(self.tmp_zip)
            self.sftp.cwd(previous_folder)
        return CodeError.SUCCESS
