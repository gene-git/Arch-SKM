# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2020-present  Gene C <arch@sapience.com>
"""
 Main class for genkeys
"""
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-few-public-methods
from typing import (Any, Dict, List, Tuple)
import os
import sys
import argparse

from .utils import file_list_glob

from .get_key_hash import get_key_hash_types

type _Opt = Tuple[str | Tuple[str, str] | Tuple[str, str, str], Dict[str, Any]]


class GenKeysBase:
    """
    Base class to create out of tree kernel signing keys
    """
    def __init__(self):
        """
        Command line args and initialize
        """
        self.cert_dir = os.path.dirname(sys.argv[0])
        self.cert_dir = os.path.abspath(self.cert_dir)
        self.cwd = os.getcwd()

        if self.cwd == self.cert_dir:
            self.config = '../config'
        else:
            self.config = './config'

        self.verb = False
        self.refresh = '7d'
        self.khash = 'sha512'
        self.ktype = 'ec'
        self.kconfig_list: List[str] = []
        self.okay = True

        #
        # parse command line options
        #
        _parse_args(self)

        #
        # Retrieve kernel module signing key and hash types
        #
        (okay, ktype, khash) = get_key_hash_types(self.kconfig_list)
        if not okay:
            self.okay = False
        self.ktype = ktype
        self.khash = khash


def _parse_args(genkeys: GenKeysBase):
    """
    Parse command line and update genekeys
     - type hint is quoted to avoid circular include
    """
    desc = os.path.basename(sys.argv[0])

    #
    # Available options
    #
    options = _avail_options(genkeys.refresh, genkeys.config)

    #
    # Add options and Parse
    #
    par = argparse.ArgumentParser(description=desc)

    for opt in options:
        opt_list, kwargs = opt
        if isinstance(opt_list, str):
            par.add_argument(opt_list, **kwargs)
        else:
            par.add_argument(*opt_list, **kwargs)

    #
    # save into genkeys
    #
    parsed = par.parse_args()
    if not parsed:
        return

    for (key, val) in vars(parsed).items():
        setattr(genkeys, key, val)

    genkeys.kconfig_list = file_list_glob(genkeys.config)
    if not genkeys.kconfig_list:
        print('No matching kernel config files found')
        genkeys.okay = False


def _avail_options(refresh: str, conf: str) -> List[_Opt]:
    """
    List of command line options.

    Args:
        refresh (str):
        Default refresh frequency

        conf (str):
        Kernel config file.
    """
    opts: List[_Opt] = []

    opts.append((('-r',  '--refresh'),
                 {'default': refresh,
                  'help': f'refresh period E.g. 7d, 24h, always. (({refresh})'
                  }
                 ))

    opts.append((('-c',  '--config'),
                 {'default': conf,
                  'help': f'Kernel Config(s). Quoted wildcards ok. ({conf})'
                  }
                 ))

    opts.append((('-v', '--verb'),
                 {'action': 'store_true',
                  'help': 'Verbose (False)'
                  }
                 ))
    #
    # deprecated options - warn to avoid any script breakage
    #
    opts.append((('-kh', '--khash'),
                 {'help': 'khash deprecated - taken from kernel config'
                  }
                 ))

    opts.append((('-kt', '--ktype'),
                 {'help': 'ktype deprecated - taken from kernel config'
                  }
                 ))

    return opts
