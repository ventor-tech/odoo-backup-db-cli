# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


# Stdlib:

import boto3
from boto3.s3.transfer import TransferConfig
from datetime import datetime, timedelta  # noqa: I001
from odoo_backup_db_cli.protocols.common import RemoteBackupHandler
from odoo_backup_db_cli.utils import CodeError


class S3BackupHandler(RemoteBackupHandler):
    """AWS Backup Handler."""

    def __init__(self):  # noqa: D107
        super().__init__()
        self.bucket = self.env.get('bucket')

    def _get_required_settings(self):
        res = super()._get_required_settings()
        res.append((
            ('bucket', 'access_key', 'secret_key'),
            'The creditials for the Amazon S3 service is not fully configured.'
        ))
        return res

    def _connect(self):
        self.client = boto3.client(
            's3',
            aws_access_key_id=self.env.get('access_key'),
            aws_secret_access_key=self.env.get('secret_key')
        )
        factor = 25
        self.transfer_config = TransferConfig(
            multipart_threshold=1024 * factor, max_concurrency=10,
            multipart_chunksize=1024 * factor, use_threads=True,
        )
        self.client.put_object(
            Bucket=self.bucket,
            Key='{0}/'.format(self.subfolder)
        )

    def _disconnect(self):
        pass  # noqa: WPS420

    def _save_db(self):
        self.client.upload_file(
            self.tmp_dump,
            self.bucket,
            '{0}/dump.sql.gz'.format(self.subfolder),
            Config=self.transfer_config
        )
        return CodeError.SUCCESS

    def _save_filestore(self):
        if self.env.get('with_filestore') not in ('False', '0', None):
            self.client.upload_file(
                self.tmp_zip,
                self.bucket,
                '{0}/filestore.zip'.format(self.subfolder),
                Config=self.transfer_config
            )
        return CodeError.SUCCESS

    def _delete_old_backups(self):  # noqa: C901, WPS231
        days = self.clean_backup_after
        folders = self.client.list_objects(Bucket=self.bucket)
        keys = []
        for subfolder in folders.get('Contents'):
            delete_date = subfolder.get('LastModified').replace(tzinfo=None) + timedelta(days)
            if delete_date < datetime.now():
                keys.append(subfolder.get('Key'))
        if keys:
            self.client.delete_objects(
                Bucket=self.bucket,
                Delete={
                    'Objects': [{'Key': key} for key in keys],
                    'Quiet': True
                }
            )
        return CodeError.SUCCESS
