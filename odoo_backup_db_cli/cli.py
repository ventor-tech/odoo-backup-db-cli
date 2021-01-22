# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

# Stdlib:
import configparser
import importlib
import logging
import os
import sys

# Thirdparty:
import click
from odoo_backup_db_cli.db_backup import dump_db, dump_filestore
from odoo_backup_db_cli.utils import (  # noqa: WPS235
    DEFAULT_BACKUPS_PATH,
    DEFAULT_CONF_PATH,
    DEFAULT_ENVIRONMENT,
    DEFAULT_FILESTORE_PATH,
    TYPES,
    CodeError,
    check_config,
    print_error_dir,
    write_config_file,
)
from yaspin import yaspin


@click.group()
def main():
    """
    Allows you to make a backup.

    Allows you to make a backup of the Odoo database and filestore once
    or set the periodicity and save it to a local or remote system.
    """


@main.command()
@click.option('--host', '-h', default='localhost', help='The server that hosts the database.')
@click.option('--port', '-p', default='5432', help='The port on which to connect to the database.')
@click.option('--username', '-u', default='odoo', help='Database username.')
@click.option('--password', '-w', default='odoo', help='Database user password.')
@click.option(
    '--path',
    '-P',
    default=DEFAULT_CONF_PATH,
    help='Path where to put the settings file.',
)
def generate_common_config(host, port, username, password, path):
    """Generates the common structure of the settings file."""
    if os.path.isfile(path):
        logging.info('The configuration file already exist.')
        return sys.exit(CodeError.FILE_ALREADY_EXIST)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    config = configparser.ConfigParser()
    dir_path = os.path.dirname(path)
    try:
        os.makedirs(dir_path, exist_ok=True)
    except OSError:  # pragma: no cover - actually tested
        print_error_dir(dir_path)
        return sys.exit(CodeError.ACCESS_DIR_ERROR)
    config[DEFAULT_ENVIRONMENT] = {
        'db_host': host,
        'db_port': port,
        'db_username': username,
        'db_password': password,
    }
    return sys.exit(write_config_file(config, path))


@main.command()
@click.option(
    '--environment',
    '-e',
    required=True,
    help=(
        'Name for the settings section, settings sections'
        ' are used for different options for saving the database.'
    ),
)
@click.option('--db-host', '-h', help='The server that hosts the database.')
@click.option('--db-port', '-p', help='The port on which to connect to the database.')
@click.option('--db-username', '-u', help='Database username.')
@click.option('--db-password', '-w', help='Database user password.')
@click.option(
    '--type',
    '-t',
    type=click.Choice(TYPES, case_sensitive=False),
    default=TYPES[0],
    help='The method by which the backup will be saved.',
)
@click.option(
    '--host',
    '-H',
    help='The server IP to which you want to save backups.',
)
@click.option(
    '--port',
    '-r',
    default='21',
    help='The server port to which you want to save backups.',
)
@click.option('--pasv', '-s', default=False, help='FTP conection mode.')
@click.option('--username', '-U', help='The server user to which you want to save backups.')
@click.option(
    '--password',
    '-W',
    help='The password of the server user to which you want to save backups.',
)
@click.option(
    '--private-key',
    '-K',
    help='The private key of the server user to which you want to save backups.',
)
@click.option(
    '--backup-location',
    '-b',
    default=DEFAULT_BACKUPS_PATH,
    help='The path where the database will be saved.',
)
@click.option(
    '--clean-backup-after',
    '-c',
    default='10',
    help="The number of days for cleaning backups. Set to '0' in need disable.",
)
@click.option(
    '--db-name',
    '-d',
    default='prod',
    help='The name of the database that will be backed up.',
)
@click.option(
    '--with-filestore/--without-filestore',
    '-F',
    default=False,
    help='If true, then in addition to the database, it will make a backup for a filestore.',
)
@click.option(
    '--filestore-location',
    '-f',
    default=DEFAULT_FILESTORE_PATH,
    help='The path to Odoo filestore',
)
@click.option(
    '--path',
    '-P',
    default=DEFAULT_CONF_PATH,
    help='Path where to put the settings file.',
)
def update_config(
    environment,
    db_host,
    db_port,
    db_username,
    db_password,
    type,
    host,
    port,
    pasv,
    username,
    password,
    private_key,
    backup_location,
    clean_backup_after,
    db_name,
    with_filestore,
    filestore_location,
    path,
):
    """
    Adding or updating the environment of the settings file.

    ATTENTION: will overwrite the environment if it exist.
    """
    if not os.path.isfile(path):
        logging.info('The configuration file does not exist.')
        return sys.exit(CodeError.FILE_DOES_NOT_EXIST)
    config = configparser.ConfigParser()
    config.read(path)
    env = {
        'db_host': db_host,
        'db_port': db_port,
        'db_username': db_username,
        'db_password': db_password,
        'type': type,
        'host': host,
        'port': port,
        'pasv': pasv,
        'username': username,
        'password': password,
        'private_key': private_key,
        'backup_location': backup_location,
        'clean_backup_after': clean_backup_after,
        'db_name': db_name,
        'with_filestore': with_filestore,
        'filestore_location': filestore_location,
    }
    config[environment] = {}
    for key, value in env.items():  # noqa: WPS110
        if value is not None:
            config[environment][key] = str(value)
    return sys.exit(write_config_file(config, path))


@main.command()
@click.argument('environment')
@click.option(
    '--path',
    '-p',
    default=DEFAULT_CONF_PATH,
    help='Use a specific config file',
)
@yaspin(text='The process of creating a backup is in progress...')
def create_backup(environment, path):
    """Creates a backup according to the settings of the selected environment."""
    if not os.path.isfile(path):
        logging.info('The configuration file does not exist.')
        return sys.exit(CodeError.FILE_DOES_NOT_EXIST)
    config = configparser.ConfigParser()
    config.read(path)
    error_found = check_config(config, environment)
    if error_found:
        return sys.exit(error_found)
    dump_db(config, environment)
    dump_filestore(config, environment)
    type = config[environment].get('type')
    plugin = importlib.import_module('odoo_backup_db_cli.protocols.{type}'.format(type=type))
    type_handler = getattr(plugin, '_{type}_handler'.format(type=type))
    type_handler(config, environment)
    return sys.exit(CodeError.SUCCESS)
