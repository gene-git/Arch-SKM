# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2020-present  Gene C <arch@sapience.com>
"""
# Support module for kernel signing tools
"""
from typing import IO
import os
import subprocess
from subprocess import SubprocessError
from datetime import datetime
import glob


def run_prog(pargs) -> tuple[int, str, str]:
    """
    Runs executable program with arguments and no shell.
    N
    Returns status along with stdout and stderr
    """
    if not pargs:
        return (0, '', 'Missing pargs')

    try:
        ret = subprocess.run(pargs,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             check=False)
    except (FileNotFoundError, SubprocessError) as err:
        return (-1, '', str(err))

    retc = ret.returncode
    output = ''
    errors = ''

    if ret.stdout:
        output = str(ret.stdout, 'utf-8', errors='ignore')

    if ret.stderr:
        errors = str(ret.stderr, 'utf-8', errors='ignore')

    return (retc, output, errors)


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
