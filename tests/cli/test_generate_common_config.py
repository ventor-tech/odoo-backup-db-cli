# -*- coding: utf-8 -*-

import configparser
import tempfile

from click.testing import CliRunner

from odoo_backup_db_cli.cli import DEFAULT_ENVIRONMENT, main


def test_generate_common_config():
    """Checking the config file."""
    runner = CliRunner()
    path = '{0}/test_conf.conf'.format(tempfile.gettempdir())
    res = runner.invoke(main, ['generate-common-config', '--path', path])
    config = configparser.ConfigParser()
    config.read(path)
    expected_config = {
        'db_host': 'localhost',
        'db_port': '5432',
        'db_username': 'odoo',
        'db_password': 'odoo',
    }
    assert res.exit_code == 0
    assert config[DEFAULT_ENVIRONMENT] == expected_config
