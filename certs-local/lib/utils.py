# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2020-present  Gene C <arch@sapience.com>
"""
# Support module for kernel signing tools
"""
from typing import IO
import os
from datetime import datetime
import glob


def date_time_now() -> datetime:
    """
    Return current datetime
    """
    today = datetime.today()
    return today


def file_list_glob(pathname: str) -> list[str]:
    """
    Return list of files match glob path
    """
    flist = glob.glob(pathname, recursive=False)
    return flist


def remove_file(fpath: str) -> bool:
    """
    Remove a file (not a dir).
    """
    if os.path.exists(fpath):
        try:
            os.unlink(fpath)
            return True
        except OSError as err:
            print(f'Failed to remove file: {fpath} Error: {err}')
            return False
    return True


def open_file(path: str, mode: str) -> IO | None:
    """
    open a file handlilng any exceptions
    Returns file object
    """
    # pylint: disable=unspecified-encoding,consider-using-with
    try:
        if 'b' in mode:
            fobj = open(path, mode)
        else:
            fobj = open(path, mode, encoding='utf-8')

    except OSError as err:
        print(f'Error opening {path}: {err}')
        fobj = None

    return fobj
