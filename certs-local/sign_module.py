#!/usr/bin/python
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2020-present  Gene C <arch@sapience.com>
"""

sign_module.py

Signs one or more kernel modules

2 use cases based on command line:

 1) list of modules to sign
    mod1 mod2 mod3 ..

 2) Directory which has list of modules
    -d <directory>

dkms uses (2)

Modules can be uncompressed (.ko) or compressed
with zstd (.zst), xz (.xz) or gzip (.gz)

Modules may also be already signed in which case the
signature is removeed before re-signing.

Supporting files need to be installed in same directory -
this is handled by install-certs.py signer_class.py and utils.py

Note:

sign_module.py is installed in each kernel build
directory under certs-local.

From the path we locate the kernel build dir and hence
the kernel (compiled) signing tool along with key information.
This is handled by the KernelModIsgner class.

i.e.
  me = '/usr/lib/modules/<kern-vers>/build/certs-local/sign_module.py'
  signer = /usr/lib/modules/<kern-vers>/build/scripts/sign-file

key files reside in current dir:
  /usr/lib/modules/<kern-vers>/build/certs-local/current/
  signing_key.pem , signing_crt.crt, khash

We use file extension to determine if/how compressed.
We do not use magic bytes.
We work in memory rather than via filesystem.
Each module is small emough its not a problem

While it may be fine to leave existing sig and sign
the (already previously) signed module - we choose to remove it.
Maybe simpler and cleaner not to bother - however, not clear if
this might cause problem for kernel sig check or not.
So we strip it out. This also removes any debug symbols
so it has a downside if the module had any debug info.
"""
import os
import sys

from lib import (ModuleTool, KernelModSigner)


def modules_from_dir(mdir: str) -> list[str]:
    """
    Get a list of kernel modules from a directory

    Returns list of (recognizable) modules located in a directory
    """
    mod_list: list[str] = []

    #
    # Includes modules with known compressed extensions
    #
    if not os.path.exists(mdir):
        print(f'Module directory bad: {mdir}')
        return mod_list

    if not os.path.isdir(mdir):
        print(f'Module directory must be a directory: {mdir}')
        return mod_list

    mod_dir = os.path.abspath(mdir)
    known_exts = ['.ko', '.ko.zst', '.ko.xz', '.ko.gz']

    try:
        scan = os.scandir(mod_dir)
    except OSError:
        print(f'Error scanning directory {mod_dir}')
        return mod_list

    for item in scan:
        if item.is_file():
            for ext in known_exts:
                if item.name.endswith(ext):
                    mod_path = os.path.join(mod_dir, item.name)
                    mod_list.append(mod_path)
                    break
    return mod_list


def parse_args(arv):
    """
    Get modules to be signed.

    Command line handling - either 1) or 2)
        1. 1 or more modules as list
        2. -d <module dir>
    """
    myname = arv[0]
    if len(arv) == 1:
        print('No modules to sign')
        return myname, None

    if arv[1] == '-d':
        if len(arv) >= 3:
            mod_dir = arv[2]
        else:
            print('Missing module dir after -d')
            return myname, None
        modules = modules_from_dir(mod_dir)
    else:
        modules = arv[1:]

    return myname, modules


def main():
    """
    sign_module: -d <dir> or mod1 mod2 ...
    """
    arv = sys.argv
    myname, modules = parse_args(arv)
    if not modules:
        print('No modules to sign')
        return

    #
    # Instantiate signer
    #
    signer = KernelModSigner(myname)
    if not signer.initialized:
        return

    #
    # sign each module from command line
    #
    for mod in modules:
        mod_tool = ModuleTool(signer, mod)
        if mod_tool.path_ok:
            okay = mod_tool.sign()
            if not okay:
                print(f'Problem signing: {mod}')
                return
        else:
            print(f'Module not found: {mod}')

    print('Success: all done')


if __name__ == '__main__':
    main()
