# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
External program execution
"""
# pylint: disable=too-many-arguments, too-many-positional-arguments
# pylint: disable=too-many-locals, too-many-branches, too-many-statements
# pylint: disable=consider-using-with
from typing import (IO)
import os
import fcntl
import io
from select import select
import subprocess
from subprocess import SubprocessError


def run_prog(pargs: list[str],
             input_str: str | None = None,
             stdout: int = subprocess.PIPE,
             stderr: int = subprocess.PIPE,
             env: dict[str, str] | None = None,
             test: bool = False,
             verb: bool = False,
             ) -> tuple[int, str, str]:
    """
    Run external program using subprocess.

    Take care to handle large outputs (default buffer size
    is 8k). This avoids possible hangs should IO buffer fill up.

    non-blocking IO together with select() loop provides
    a robust methodology.

    Args:
        pargs (list[str]):
            The command + arguments to be run in standard list format.
            e.g. ['/usr/bin/sleep', '22'].

        input_str (str | None):
            Optional input to be fed to subprocess stdin.  Defaults to None.

        stdout (int):
            Subprocess stdout. Defaults to subprocess.PIPE

        stderr (int):
            Subprocess stderr. Defaults to subprocess.PIPE

        env (None | dict[str, str]):
            Optional to specify environment for subprocess to use.
            If not set, inherits from calling process as usual.

        test (bool):
            Flag - if true dont actually run anything.

        verb (bool):
            Flag - only used with test == True - prints pargs.

    Returns:
        tuple[retc: int, stdout: str, stderr: str]:
            retc is 0 when all is well.
            stdout is what the subprocess returns on it's stdout
            and stderr is what it's stderr return.

    Note that any input string is written in it's entirety in one
    shot to the subprocess. This should not be a problem.
    """
    if not pargs:
        return (0, '', '')

    if test:
        if verb:
            print(' '.join(pargs))
        return (0, '', '')

    #
    # Tee up any input - even if no "input string"
    # If no input string and process expects input
    # it would hang without input - so we always allow it.
    # Select() will tell us whether process needs it.
    #
    bstring: bytes | None = None
    stdin: int | None = None
    if input_str:
        bstring = input_str.encode('utf-8')
        stdin = subprocess.PIPE

    retc: int = -1
    output: str = ''
    errors: str = ''

    #
    # Start up the process
    #
    (okay, proc, errors) = _popen_proc(pargs, stdin, stdout, stderr, env)

    if not okay:
        return (1, '', errors)

    #
    # Wait for it to complete
    # - we handle large output buffers by using non-blocking IO
    #   and select() along with reading buffer/pipe to ensure
    #   it never fills up and blocks.
    #   Without this, larger output can hang hwne IO buffer is full.
    #

    (retc, output, errors) = _wait_for_proc(bstring, proc)

    return (retc, output, errors)


def _popen_proc(pargs: list[str],
                stdin: int | None,
                stdout: int = subprocess.PIPE,
                stderr: int = subprocess.PIPE,
                env: dict[str, str] | None = None,
                ) -> tuple[bool, subprocess.Popen | None, str]:
    """
    Popen the process to run

    Args:
        See run_prog()

    Returns:
        tuple[success: bool, proc: subprocess.Popen , error: str]
    """
    #
    # Popen the process
    #
    proc: subprocess.Popen | None = None
    try:
        proc = subprocess.Popen(pargs,
                                stdin=stdin,
                                stdout=stdout,
                                stderr=stderr,
                                env=env)

    except (OSError, FileNotFoundError, ValueError, SubprocessError) as err:
        return (False, proc, str(err))

    return (True, proc, '')


def _wait_for_proc(bstring: bytes | None,
                   proc: subprocess.Popen | None) -> tuple[int, str, str]:
    """
    Process has been opened, wait for process to complete.

    Args:
        proc (subprocess.Popen):

    Returns:
        tuple[returncode: int, stdout: str, stderr: str]
    """
    output = ''
    errors = ''
    timeout = 30
    bufsiz = io.DEFAULT_BUFFER_SIZE

    if not proc:
        return (-1, '', 'process not started by popen - giving up')

    returncode = proc.returncode
    has_stdout = True
    has_stderr = True
    has_stdin = bool(bstring)

    try:
        if proc.stdin:
            fcntl.fcntl(proc.stdin, fcntl.F_SETFL, os.O_NONBLOCK)

        if proc.stdout:
            fcntl.fcntl(proc.stdout, fcntl.F_SETFL, os.O_NONBLOCK)

        if proc.stderr:
            fcntl.fcntl(proc.stderr, fcntl.F_SETFL, os.O_NONBLOCK)

    except OSError as err:
        # Should not happen. Cross fingers and keep going.
        print(f'Error setting NONBLOCK: {err}')

    data_pending = bool(has_stdout or has_stderr or has_stdin)

    while returncode is None or data_pending:
        returncode = proc.poll()

        if returncode:
            continue

        readlist: list[int | IO] = []
        if has_stdout and proc.stdout:
            readlist.append(proc.stdout)

        if has_stderr and proc.stderr:
            readlist.append(proc.stderr)

        writelist: list[int | IO] = []
        if has_stdin and proc.stdin:
            writelist = [proc.stdin]

        exceplist: list[int | IO] = []

        if not (readlist or writelist or exceplist):
            data_pending = False
            continue

        try:
            ready = select(readlist, writelist, exceplist, timeout)
            read_ready = ready[0]
            write_ready = ready[1]

            try:
                if has_stdin and proc.stdin and proc.stdin in write_ready:
                    proc.stdin.write(bstring)
                    proc.stdin.flush()
                    proc.stdin.close()
                    has_stdin = False

                if has_stdout and proc.stdout and proc.stdout in read_ready:
                    data = proc.stdout.read(bufsiz)
                    if len(data) == 0:
                        has_stdout = False
                        proc.stdout.close()
                    else:
                        output += str(data, 'utf-8', errors='ignore')

                if has_stderr and proc.stderr and proc.stderr in read_ready:
                    data = proc.stderr.read(bufsiz)
                    if len(data) == 0:
                        has_stderr = False
                        proc.stderr.close()
                    else:
                        errors += str(data, 'utf-8', errors='ignore')

                data_pending = bool(has_stdout or has_stderr or has_stdin)

            except (OSError, IOError, EOFError, ValueError) as err:
                # read/write
                return (-1, output, str(err) + ':\n' + errors)

        except OSError as err:
            # select
            return (-1, output, str(err) + ':\n' + errors)

    # all done.
    retc = proc.returncode
    return (retc, output, errors)
