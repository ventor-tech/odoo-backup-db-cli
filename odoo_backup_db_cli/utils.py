# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from enum import IntEnum


class CodeError(IntEnum):
    """List of possible program crashes."""

    SUCCESS = 0
    ACCESS_DIR_ERROR = 1
    ACCESS_FILE_ERROR = 2
    FILE_ALREADY_EXIST = 3
    FILE_DOES_NOT_EXIST = 4
    NO_SETTINGS = 5
    INVALID_SETTINGS = 6
