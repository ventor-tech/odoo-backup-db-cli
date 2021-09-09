# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import tempfile
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

FORMAT_TIME = '%Y-%m-%d-%H-%M-%S'


class BackupHandler(ABC):
    """BackupHandler"""

    def __init__(self, config, env):
        self.config = config
        self.protocol = env
        self.env = env in config and config[env] or config['common']
        self.with_filestore = self.env.get('with_filestore') not in ('False', '0', None)
        self.with_db = self.env.get('with_db') not in ('False', '0', None)
        self.clean_backup_after = int(self.env.get('clean_backup_after', 7))
        self.tmp_dump = '{0}/dump.sql.gz'.format(tempfile.gettempdir())
        self.tmp_zip = '{0}/filestore.zip'.format(tempfile.gettempdir())
        self.subfolder = datetime.now().strftime(FORMAT_TIME)

    def _get_required_settings(self):
        return [
            ('clean_backup_after', 'The settings do not indicate where to save the backup.')
        ]

    def check_config(self):
        if not self.env:
            raise Exception('Not found [{}] config section'.format(self.protocol))

        for name, info in self._get_required_settings():
            options = name if type(name) is tuple else (name,)
            for opt_name in options:
                if self.env.get(opt_name) is None:
                    raise Exception('Not found {}. {}'.format(opt_name, info))

        if self.with_filestore and not self.env.get('filestore_location'):
            raise Exception(
                'Not found filestore_location. '
                'The settings do not indicate where to exist the filestore.'
            )

        if self.with_db:
            for opt_name in ['db_port', 'db_username', 'db_password', 'db_host', 'db_name']:
                if self.env.get(opt_name) is None:
                    raise Exception(
                        'Not found {}. '
                        'The creditials of the database is not fully configured.'.format(opt_name)
                    )

    @abstractmethod
    def _save_db(self):
        pass

    @abstractmethod
    def _save_filestore(self):
        pass

    @abstractmethod
    def _delete_old_backups(self):
        pass

    def _is_folder_to_remove(self, folder):
        try:
            correct_folder = datetime.strptime(folder, FORMAT_TIME)
        except ValueError:
            return False

        if correct_folder + timedelta(self.clean_backup_after) >= datetime.now():
            return False

        return True

    def run(self):
        if self.with_db:
            self._save_db()
        if self.with_filestore:
            self._save_filestore()
        self._delete_old_backups()


class RemoteBackupHandler(BackupHandler):
    '''
        for ftp, sftp, s3 protocols
    '''

    def run(self):
        self._connect()
        try:
            super(RemoteBackupHandler, self).run()
        finally:
            self._disconnect()


class FSBackupHandler(BackupHandler):
    '''
        (File System type) for local, ftp, sftp protocols
    '''

    def __init__(self, config, env):
        super(FSBackupHandler, self).__init__(config, env)
        self.backup_location = self.env.get('backup_location')

    def _get_required_settings(self):
        res = super(FSBackupHandler, self)._get_required_settings()
        res.append(
            ('backup_location', 'The settings do not indicate where to save the backup.'),
        )
        return res
