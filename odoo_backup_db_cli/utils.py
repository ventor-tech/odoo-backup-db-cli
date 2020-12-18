# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from enum import IntEnum


class CodeError(IntEnum):
    """List of possible program crashes."""

    SUCCESS = 0
    ACCESS_ERROR = 1
    FILE_ALREADY_EXIST = 2
    FILE_DOES_NOT_EXIST = 3
    NO_SETTINGS = 4
    INVALID_SETTINGS = 5
