# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

# Stdlib:
import os
import tempfile
import boto3
from datetime import datetime, timedelta
from boto3.s3.transfer import TransferConfig

# Thirdparty:
from odoo_backup_db_cli.utils import CodeError

FORMAT_TIME = '%Y-%m-%d-%H-%M-%S'
transfer_config = TransferConfig(multipart_threshold=1024*25, max_concurrency=10,
    multipart_chunksize=1024*25, use_threads=True)


def _s3_save_db(config, environment, client, subfolder):
    client.upload_file(
        '{0}/dump.sql'.format(tempfile.gettempdir()),
        config[environment].get('bucket'),
        '{}/dump.sql'.format(subfolder),
        Config=config
    )
    return CodeError.SUCCESS


def _s3_save_filestore(config, environment, client, subfolder):
    if config[environment].get('with_filestore') not in ('False', '0', None):
        client.upload_file(
            '{0}/filestore.zip'.format(tempfile.gettempdir()),
            config[environment].get('bucket'),
            '{}/filestore.zip'.format(subfolder),
            Config=config
        )
    return CodeError.SUCCESS


def _s3_delete_old_backups(config, environment, client):  # noqa: C901, WPS231
    days = int(config[environment].get('clean_backup_after'))
    folders = client.list_objects(Bucket=config[environment].get('bucket'))
    for subfolder in folders.get('Contents'):
        if subfolder.get('LastModified') + timedelta(days) < datetime.now():
            client.delete_objects(
                Bucket=config[environment].get('bucket'),
                Delete=subfolder.get('Key')
            )
    return CodeError.SUCCESS


def _s3_handler(config, environment):
    client = boto3.client(
        's3',
        aws_access_key_id=config[environment].get('access_key'),
        aws_secret_access_key=config[environment].get('secret_key')
    )
    config = TransferConfig(multipart_threshold=1024*25, max_concurrency=10,
        multipart_chunksize=1024*25, use_threads=True)
    subfolder = datetime.now().strftime(FORMAT_TIME)
    client.put_object(Bucket=config[environment].get('bucket'), Key=(subfolder+'/'))
    _s3_save_db(config, environment, client, subfolder)
    _s3_save_filestore(config, environment, client, subfolder)
    _s3_delete_old_backups(config, environment, client)
    # ftp.quit()
    return CodeError.SUCCESS
