# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import ftplib  # noqa: S402
import os
import tempfile
from datetime import datetime, timedelta

FORMAT_TIME = '%Y-%m-%d-%H-%M-%S'


def _ftp_mk_dirs(current_dir, ftp):
    if current_dir != '':
        try:
            ftp.cwd(current_dir)
        except ftplib.Error:
            _ftp_mk_dirs('/'.join(current_dir.split('/')[:-1]), ftp)
            ftp.mkd(current_dir)
            ftp.sendcmd('SITE CHMOD 755 {0}'.format(current_dir))
            ftp.cwd(current_dir)


def _ftp_save_db(config, environment, ftp, subfolder):
    _ftp_mk_dirs(config[environment].get('backup_location'), ftp)
    if subfolder not in ftp.nlst():
        ftp.mkd(subfolder)
    previous_folder = ftp.pwd()
    ftp.cwd(subfolder)
    with open('{0}/dump.sql'.format(tempfile.gettempdir()), 'rb') as dump:
        ftp.storbinary('STOR dump.sql', dump)
    os.remove('{0}/dump.sql'.format(tempfile.gettempdir()))
    ftp.cwd(previous_folder)


def _ftp_save_filestore(config, environment, ftp, subfolder):
    if config[environment].get('with_filestore') not in ('False', '0', None):
        previous_folder = ftp.pwd()
        ftp.cwd(subfolder)
        with open('{0}/filestore.zip'.format(tempfile.gettempdir()), 'rb') as filestore:
            ftp.storbinary('STOR filestore.zip', filestore)
        os.remove('{0}/filestore.zip'.format(tempfile.gettempdir()))
        ftp.cwd(previous_folder)


def _ftp_delete_old_backups(config, environment, ftp):
    days = int(config[environment].get('clean_backup_after'))
    if days:
        for folder in ftp.nlst():
            if datetime.strptime(folder, FORMAT_TIME) + timedelta(days) < datetime.now():
                for ftp_file in list(ftp.nlst(folder)):
                    ftp.delete(ftp_file)
                ftp.rmd(folder)


def _ftp_handler(config, environment):
    ftp = ftplib.FTP()  # noqa: S321
    ftp.connect(config[environment].get('host'), int(config[environment].get('port')))
    ftp.login(config[environment].get('username'), config[environment].get('password'))
    pasv = False if config[environment].get('pasv') in ('False', '0', None) else True
    ftp.set_pasv(pasv)
    subfolder = datetime.now().strftime(FORMAT_TIME)
    _ftp_save_db(config, environment, ftp, subfolder)
    _ftp_save_filestore(config, environment, ftp, subfolder)
    _ftp_delete_old_backups(config, environment, ftp)
    ftp.quit()
