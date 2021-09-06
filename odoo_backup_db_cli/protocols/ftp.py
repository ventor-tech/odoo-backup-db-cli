# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

# Stdlib:
import ftplib  # noqa: S402
import os

# Thirdparty:
from odoo_backup_db_cli.protocols.common import RemoteBackupHandler, FSBackupHandler


class FtpBackupHandler(RemoteBackupHandler, FSBackupHandler):

    def _get_required_settings(self):
        res = super(FtpBackupHandler, self)._get_required_settings()
        res.append(
            (
                ('username', 'password', 'host', 'port', 'pasv'),
                'The creditials for the ftp server is not fully configured.'
            )
        )
        return res

    def _connect(self):
        self.ftp = ftplib.FTP()  # noqa: S321
        self.ftp.connect(
            self.env.get('host'),
            int(self.env.get('port'))
        )
        self.ftp.login(
            self.env.get('username'),
            self.env.get('password')
        )
        pasv = False if self.env.get('pasv') in ('False', '0', None) else True
        self.ftp.set_pasv(pasv)

    def _disconnect(self):
        self.ftp.quit()

    def _ftp_mk_dirs(self, current_dir):
        if current_dir != '':
            try:
                self.ftp.cwd(current_dir)
            except ftplib.Error:
                self._ftp_mk_dirs('/'.join(current_dir.split('/')[:-1]))
                self.ftp.mkd(current_dir)
                self.ftp.sendcmd('SITE CHMOD 755 {0}'.format(current_dir))
                self.ftp.cwd(current_dir)

    def _save_db(self):
        self._ftp_mk_dirs(self.backup_location)
        if subfolder not in self.ftp.nlst():
            self.ftp.mkd(subfolder)
        previous_folder = ftp.pwd()
        self.ftp.cwd(subfolder)
        with open(self.tmp_dump, 'rb') as dump:
            self.ftp.storbinary('STOR dump.sql.gz', dump)
        os.remove(self.tmp_dump)
        self.ftp.cwd(previous_folder)

    def _save_filestore(self):
        if self.with_filestore:
            previous_folder = ftp.pwd()
            self.ftp.cwd(self.subfolder)
            with open(tmp_zip, 'rb') as filestore:
                self.ftp.storbinary('STOR filestore.zip', filestore)
            os.remove(tmp_zip)
            self.ftp.cwd(previous_folder)

    def _delete_old_backups(config, environment, ftp):  # noqa: C901, WPS231
        for folder in ftp.nlst():  # pragma: no cover - actually tested
            if self._is_folder_to_remove(folder):
                for ftp_file in list(self.ftp.nlst(folder)):
                    self.ftp.delete(ftp_file)
                self.ftp.rmd(folder)
