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

def color_error_msg(msg):
    return '\033[91m{}\033[0m'.format(msg)
