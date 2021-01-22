# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

# Stdlib:
import logging
from enum import IntEnum
from pathlib import Path

DEFAULT_CONF_PATH = '/etc/odoo/odoo_backup.conf'
DEFAULT_FILESTORE_PATH = '/opt/odoo/.local/share/Odoo/filestore/'
DEFAULT_BACKUPS_PATH = '/var/opt/odoo/backups'
DEFAULT_ENVIRONMENT = 'common'
TYPES = ('local', 'ftp', 'sftp')


class CodeError(IntEnum):
    """List of possible program crashes."""

    SUCCESS = 0
    ACCESS_DIR_ERROR = 1
    ACCESS_FILE_ERROR = 2
    FILE_ALREADY_EXIST = 3
    FILE_DOES_NOT_EXIST = 4
    NO_SETTINGS = 5
    INVALID_SETTINGS = 6


def print_error_dir(dir_path):  # pragma: no cover - actually tested
    """Print details about error dir."""
    logging.info('Creation of the directory "{0}" failed.'.format(dir_path))
    logging.info('Please change access rights or owner for parent directory and try again.')
    logging.info('If you want change access rights, probably next command help you.')
    logging.info('Run it: "sudo chmod ugo+w {0}".'.format(Path(dir_path).parent))
    logging.info('If you want change owner, probably next command help you.')
    logging.info('Run it: "sudo chown -R $USER {0}".'.format(Path(dir_path).parent))


def print_error_file(path):
    """Print details about error file."""
    logging.info('Creation of the file "{0}" failed.'.format(path))
    logging.info('Please change access rights or owner for parent directory and try again.')
    logging.info('If you want change access rights, probably next command help you.')
    logging.info('Run it: "sudo chmod ugo+w {0}".'.format(Path(path).parent))
    logging.info('If you want change owner, probably next command help you.')
    logging.info('Run it: "sudo chown -R $USER {0}".'.format(Path(path).parent))


def write_config_file(config, path):
    """Writes new config changes."""
    try:
        with open(path, 'w') as configfile:
            config.write(configfile)
    except OSError:
        print_error_file(path)
        return CodeError.ACCESS_FILE_ERROR
    else:
        return CodeError.SUCCESS


def check_config(config, environment):  # noqa: C901, WPS212, WPS210, WPS213, WPS231
    """Checks for the validity of the config."""
    if environment not in config.sections():
        logging.info('The selected environment does not exist.')
        return CodeError.NO_SETTINGS
    backup_location = config[environment].get('backup_location')
    if backup_location is None:
        logging.info('The settings do not indicate where to save the backup.')
        return CodeError.NO_SETTINGS
    clean_backup_after = config[environment].get('clean_backup_after')
    if clean_backup_after is None:
        logging.info('The settings do not indicate after how many days to delete.')
        return CodeError.NO_SETTINGS
    elif not clean_backup_after.isdecimal():
        logging.info('The clean_backup_after parameter should be digit.')
        return CodeError.INVALID_SETTINGS
    if config[environment].get('with_filestore') not in ('False', '0', None):
        filestore_location = config[environment].get('filestore_location')
        if filestore_location is None:
            logging.info('The settings do not indicate where to exist the filestore.')
            return CodeError.NO_SETTINGS
    all_config_fields = set(config[environment].keys()).union(
        set(config[DEFAULT_ENVIRONMENT].keys())
    )
    db_fields = {'db_port', 'db_username', 'db_password', 'db_host', 'db_name'}
    if not db_fields.issubset(all_config_fields):
        logging.info('The creditials of the database is not fully configured.')
        return CodeError.NO_SETTINGS
    type = config[environment].get('type')
    if type not in TYPES:
        logging.info('Connection type is not corrected in the settings.')
        logging.info('You should choose between {0}.'.format(TYPES))
        return CodeError.NO_SETTINGS
    elif type == 'ftp':
        ftp_fields = {'username', 'password', 'host', 'port', 'pasv'}
        if not ftp_fields.issubset(all_config_fields):
            logging.info('The creditials for the ftp server is not fully configured.')
            logging.info('Next fields are required: {0}.'.format(ftp_fields))
            return CodeError.NO_SETTINGS
    elif type == 'sftp':
        auth_types = {'private_key', 'password'}
        if auth_types.issubset(all_config_fields):
            logging.info(
                'Only one of these fields must be present in settings environment: {0}'.format(
                    auth_types
                )
            )
            return CodeError.INVALID_SETTINGS
        sftp_fields = {'username', 'host', 'port', 'pasv'}
        is_missing_field = not sftp_fields.issubset(all_config_fields)
        is_missing_auth_type = not auth_types.intersection(all_config_fields)
        if is_missing_field or is_missing_auth_type:
            logging.info('The creditials for the ftp server is not fully configured.')
            logging.info('Next fields are required: {0}.'.format(sftp_fields.union(auth_types)))
            return CodeError.NO_SETTINGS
    return CodeError.SUCCESS
