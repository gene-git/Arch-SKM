# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2020-present  Gene C <arch@sapience.com>
"""
 Extract kernel config signing key / hash
"""
from typing import (List, Tuple)

from .utils import open_file


def get_key_hash_types(kconfig_list: List[str]
                       ) -> Tuple[bool, str, str]:
    """
    Read kernel config to determine:

     - module signing key type
     - module hash type

    Args:
        kconfig_list (List[str]):
        List of kernel config files.

    Returns:
        Tuple[okay: bool, key_type: str, hash_type: str]:
        Okay is True when key and hash types are found.

    """

    #
    # multiple config support added by request.
    # Config name came from reading dir, failing to open would be unlikely
    # If multiple configs, then check all using same key/hash types
    #
    all_okay = True
    key_type = ''
    hash_type = ''

    for kconfig in kconfig_list:
        (okay, ktype, htype) = _parse_config_file(kconfig)

        if not okay:
            print(f'Failed to open: {kconfig}')
            all_okay = False
            continue

        # save key type
        if not key_type:
            key_type = ktype

        elif ktype != key_type:
            err = 'key_types must be same across configs'
            print(f'{err}: {key_type} vs {ktype}')

        # save hash type
        if not hash_type:
            hash_type = htype

        elif htype != hash_type:
            err = 'hash_types must be same across configs'
            print(f'{err}: {hash_type} vs {htype}')

    # did we find both
    if not (key_type and hash_type):
        all_okay = False

    return (all_okay, key_type, hash_type)


def _parse_config_file(kconfig: str) -> Tuple[bool, str, str]:
    """
    Read one kernel config to determine:

     - module signing key type
     - module hash type

    Args:
        kconfig (str):
        A kernel config files.

    Returns:
        Tuple[okay: bool, key_type: str, hash_type: str]:
        Okay is True when key and hash types are found.

    """
    all_okay = True

    key_type = ''
    hash_type = ''

    fobj = open_file(kconfig, 'r')
    if fobj:
        conf_lines = fobj.readlines()
        fobj.close()
    else:
        print(f'Failed to open: {kconfig}')
        all_okay = False
        return (False, key_type, hash_type)

    #
    # Find the hash and key type lines
    #
    num_to_find = 2
    count = 0
    for config_line in conf_lines:

        (okay, ktype, htype) = _parse_one(config_line)
        if not okay:
            all_okay = False
            print(f'Error in {kconfig}: {config_line}')
            continue

        if ktype:
            count += 1
            if not key_type:
                key_type = ktype
            elif ktype != key_type:
                err = 'key_types must be same across configs'
                print(f'{err}: {key_type} vs {ktype}')

        if htype:
            count += 1
            if not hash_type:
                hash_type = htype
            elif ktype != hash_type:
                err = 'hash_types must be same across configs'
                print(f'{err}: {hash_type} vs {htype}')

        if count >= num_to_find:
            # all done for this config file
            break

    if count < num_to_find:
        print(f' Failed to find kernel sign key or hash type: {kconfig}')
        all_okay = False

    return (all_okay, key_type, hash_type)


def _parse_one(line: str) -> Tuple[bool, str, str]:
    """
    Parse one config line for key / hash type
    """

    key_type = ''
    hash_type = ''

    all_okay = True

    (okay, key_type) = _config_to_key_type(line)
    if not okay:
        all_okay = False

    (okay, hash_type) = _config_to_hash_type(line)
    if not okay:
        all_okay = False

    return (all_okay, key_type, hash_type)


def _config_to_key_type(config_line: str) -> Tuple[bool, str]:
    """
    Identify key type from kernel config row
    with "CONFIG_MODULE_SIG_KEY_TYPE_"
    """
    ktype = ''
    if not config_line.startswith('CONFIG_MODULE_SIG_KEY_TYPE_'):
        return (True, ktype)

    csplit = config_line.split('=')
    name = csplit[0]
    if name.endswith('RSA'):
        ktype = 'rsa'

    elif name.endswith('ECDSA'):
        ktype = 'ec'

    else:
        print(f'Unknown kernel config {config_line}')
        return (False, ktype)

    return (True, ktype)


def _config_to_hash_type(config_line: str) -> Tuple[bool, str]:
    """
    Identify hash type from kernel config row
    with "CONFIG_MODULE_SIG_HASH"
    """
    hash_type = ''
    if not config_line.startswith('CONFIG_MODULE_SIG_HASH'):
        return (True, hash_type)

    csplit = config_line.split('=')
    hash_type = csplit[1]
    hash_type = hash_type.strip().strip('"')
    if not hash_type:
        return (False, hash_type)
    return (True, hash_type)
