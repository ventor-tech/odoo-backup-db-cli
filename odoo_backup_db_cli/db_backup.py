# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

# Stdlib:
import os
import shutil
import subprocess
import tempfile

# Thirdparty:
from odoo_backup_db_cli.utils import DEFAULT_ENVIRONMENT, CodeError


def dump_db(config, environment):
    """Makes a copy of the database."""
    db_config = (
        config[environment].get('db_username', config[DEFAULT_ENVIRONMENT].get('db_username')),
        config[environment].get('db_password', config[DEFAULT_ENVIRONMENT].get('db_password')),
        config[environment].get('db_host', config[DEFAULT_ENVIRONMENT].get('db_host')),
        config[environment].get('db_port', config[DEFAULT_ENVIRONMENT].get('db_port')),
        config[environment].get('db_name'),
    )
    temp_dir = tempfile.gettempdir()
    script = ''.join(
        [
            '#!/bin/bash\n\n',
            'echo "{3}:{4}:{5}:{1}:{2}" > {0}/.pgpass\n'.format(temp_dir, *db_config),
            'chmod 0600 {0}/.pgpass\n'.format(temp_dir),
            'PGPASSFILE={0}/.pgpass\n'.format(temp_dir),
            'export PGPASSFILE\n',
            'pg_dump -U {1} -h {3} -p {4} {5} > {0}/dump.sql\n'.format(
                temp_dir,
                *db_config,
            ),
        ]
    )
    subprocess.call(script, shell=True)
    os.remove('{0}/.pgpass'.format(temp_dir))
    return CodeError.SUCCESS


def dump_filestore(config, environment):
    """Makes a copy of the filestore."""
    if config[environment].get('with_filestore') not in ('False', '0', None):
        filestore = os.path.join(
            config[environment].get('filestore_location'),
            config[environment].get('db_name'),
        )
        shutil.make_archive('{0}/filestore'.format(tempfile.gettempdir()), 'zip', filestore)
    return CodeError.SUCCESS
