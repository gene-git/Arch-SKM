#!/usr/bin/python
# SPDX-License-Identifier: MIT
# Copyright (c) 2020-2023 Gene C
"""
 install_certs.py

 Called from package_headers()

 Installs the current keys and signing scripts.
   .. certs-local/current -> dest_dir
   .. certs-local/sign_module.py -> dest_dir
   .. certs-local/lib -> dest_dir

 Takes 1 Argument which is the destination directory
 Must reside in same certs-local directory with key/certs.

 To be used in PKGBUILD

 The destination directory will be created if it doesn't exist

"""
# pylint: disable=C0103
# Gene 2022-04-31
#
import os
import sys
from lib import run_prog

#
# Extract self dir and dest dir
#
def _parse_args(arv):

    err = None
    src_dir = None
    dst_dir = None
    # check dest dir
    if len(arv) < 2:
        err = 'Missing destination dir'

    dst_dir = arv[1]
    if os.path.exists(dst_dir) and not os.path.isdir(dst_dir):
        err = 'Bad destination - is not a dir : ' + dst_dir

    if err:
        print (err)
    else:
        os.makedirs(dst_dir, exist_ok=True)
        src_dir = os.path.dirname(arv[0])
        src_dir = os.path.abspath(src_dir)

    return src_dir, dst_dir

def _run_prog_verb(pargs):

    okay = True
    [retc, _stdout, stderr] = run_prog(pargs)
    if retc != 0:
        okay = False
        print ('Error  with : ' + ' ' .join(pargs))
        if stderr:
            print(stderr)

    return okay

def main():
    """
     install_certs
     Installs certificates and tools needed to sign module
    """
    src_dir,dst_dir = _parse_args(sys.argv)
    if not dst_dir:
        return

    cur_path = os.path.join(src_dir, 'current')
    key_dir = os.readlink(cur_path)
    key_dir = os.path.join(src_dir, key_dir)
    key_dir = os.path.abspath(key_dir)

    signer = os.path.join(src_dir, 'sign_module.py')
    lib = os.path.join(src_dir, 'lib')

    # list of things to copy to dst_dir
    flist = [cur_path, key_dir, signer, lib]
    pargs = ['/usr/bin/rsync', '-a'] + flist + [dst_dir]

    okay = _run_prog_verb(pargs)
    if not okay:
        return

    return


# ----------------------------
if __name__ == '__main__':
    main()
# ----------------------------
