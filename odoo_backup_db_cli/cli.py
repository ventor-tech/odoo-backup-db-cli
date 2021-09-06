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
    CodeError,
    print_error_dir,
    write_config_file,
    color_error_msg
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
        sys.exit(color_error_msg('The configuration file already exist.'))
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
    '--bucket',
    '-B',
    help='The Amazon S3 bucket name to which you want to save backups.',
)
@click.option(
    '--access-key',
    '-A',
    help='The AWS access key.',
)
@click.option(
    '--secret-key',
    '-S',
    help='The AWS secret key.',
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
    '--with-filestore',
    '-F',
    default=False,
    help='If true, then it will make a backup for a filestore.',
)
@click.option(
    '--with-db',
    '-D',
    default=False,
    help='If true, then it will make a backup of the database.',
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
    host,
    port,
    pasv,
    username,
    password,
    private_key,
    bucket,
    access_key,
    secret_key,
    backup_location,
    clean_backup_after,
    db_name,
    with_filestore,
    with_db,
    filestore_location,
    path,
):
    """
    Adding or updating the environment of the settings file.

    ATTENTION: will overwrite the environment if it exist.
    """
    if not os.path.isfile(path):
        sys.exit(color_error_msg('The configuration file does not exist.'))
    config = configparser.ConfigParser()
    config.read(path)
    env = {
        'db_host': db_host,
        'db_port': db_port,
        'db_username': db_username,
        'db_password': db_password,
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
        'with_db': with_db,
        'filestore_location': filestore_location,
    }
    self.env = {}
    for key, value in env.items():  # noqa: WPS110
        if value is not None:
            self.env[key] = str(value)
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
        sys.exit(
            color_error_msg(
                'The configuration file {} does not exist.'.format(path)
            )
        )

    config = configparser.ConfigParser(default_section='common', allow_no_value=True)
    config.read(path)
    try:
        plugin = getattr(
            importlib.import_module(
                'odoo_backup_db_cli.protocols.{env}'.format(
                    env=environment
                )
            ),
            '{env}BackupHandler'.format(env=environment.capitalize())
        )
    except ModuleNotFoundError:
        sys.exit('Plugin for {} if not implemented yet.')
    handler = plugin(config, environment)

    try:
        handler.check_config()
    except Exception as e:
        sys.exit(color_error_msg(e))

    if config[environment].get('with_db'):
        dump_db(config, environment)
    if config[environment].get('with_filestore'):
        dump_filestore(config, environment)

    handler.run()
    sys.exit(0)
