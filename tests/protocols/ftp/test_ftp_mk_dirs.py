# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

# Stdlib:
import tempfile

# Thirdparty:
from mock import call, patch
from odoo_backup_db_cli.protocols.ftp import _ftp_mk_dirs, ftplib
from odoo_backup_db_cli.utils import CodeError


def cwd_result_generator():
    raise ftplib.Error
    yield 0


gen = cwd_result_generator()


def sideeffect(test):
    global gen
    for x in gen:
        return x


@patch.object(ftplib.FTP, 'cwd', side_effect=sideeffect)
@patch.object(ftplib.FTP, 'mkd')
@patch.object(ftplib.FTP, 'sendcmd')
def test_ok(sendcmd_mock, mkd_mock, cmd_mock):
    path = '{0}/test_ftp_mk_dirs'.format(tempfile.gettempdir())
    res = _ftp_mk_dirs(path, ftplib.FTP)
    sendcmd_mock.assert_called_once()
    mkd_mock.assert_called_once()
    cmd_mock.assert_has_calls([call(path), call(tempfile.gettempdir())])
    assert res == CodeError.SUCCESS


def test_empty():
    path = ''
    res = _ftp_mk_dirs(path, ftplib.FTP)
    assert res == CodeError.SUCCESS
