# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
External program execution
"""
# pylint: disable=too-many-arguments, too-many-positional-arguments
import subprocess


try:
    import pyconcurrent

    def run_prog(
            pargs: list[str],
            input_str: str | None = None,
            stdout: int = subprocess.PIPE,
            stderr: int = subprocess.PIPE,
            env: dict[str, str] | None = None,
            test: bool = False,
            verb: bool = False
            ) -> tuple[int, str, str]:
        """
        Run external program using subprocess - via pyconcurrent module..
        """
        return pyconcurrent.run_prog(
                pargs,
                input_str,
                stdout=stdout,
                stderr=stderr,
                env=env,
                test=test,
                verb=verb)

except ImportError:
    from .run_prog_copy import run_prog as run_prog_copy

    def run_prog(
                pargs: list[str],
                input_str: str | None = None,
                stdout: int = subprocess.PIPE,
                stderr: int = subprocess.PIPE,
                env: dict[str, str] | None = None,
                test: bool = False,
                verb: bool = False
                ) -> tuple[int, str, str]:
        """
        Run external program using subprocess - via pyconcurrent module..
        """
        return run_prog_copy(
                pargs,
                input_str,
                stdout=stdout,
                stderr=stderr,
                env=env,
                test=test,
                verb=verb)
