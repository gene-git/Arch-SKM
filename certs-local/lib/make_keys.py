# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2020-present  Gene C <arch@sapience.com>
"""
Generate any neeed keys.
"""
import os
from dataclasses import dataclass
import stat
import uuid

from ._genkeys_base import GenKeysBase
from .run_prog import run_prog
from .utils import open_file
from .utils import date_time_now


@dataclass
class KeyInfo:
    """ key information """
    kvalid: str
    kx509: str
    kprv: str
    kkey: str
    kcrt: str
    khash: str
    ktype: str


def _create_new_keys(keyinfo: KeyInfo, verb: bool) -> bool:
    """
    Make the actual keys - rsa or ec using openssl
    """
    # pylint: disable=R0913
    okay = True

    kvalid = keyinfo.kvalid
    kx509 = keyinfo.kx509
    kprv = keyinfo.kprv
    kkey = keyinfo.kkey
    kcrt = keyinfo.kcrt

    khash = keyinfo.khash
    ktype = keyinfo.ktype

    # new key
    cmd = f'/usr/bin/openssl req -new -nodes -utf8 -{khash} -days {kvalid}'
    cmd = cmd + f' -batch -x509 -config {kx509}'
    cmd = cmd + f' -outform PEM -out {kkey} -keyout {kkey}'

    if ktype == 'ec':
        cmd = cmd + ' -newkey ec -pkeyopt ec_paramgen_curve:secp384r1'

    pargs = cmd.split()
    (retc, _stdout, stderr) = run_prog(pargs)
    if retc != 0:
        print('Error making new key')
        if verb and stderr:
            print(stderr)
        return not okay

    os.chmod(kkey, stat.S_IREAD | stat.S_IWRITE)

    # extract private key
    cmd = f'/usr/bin/openssl pkey -in {kkey} -out {kprv}'
    pargs = cmd.split()
    (retc, _stdout, stderr) = run_prog(pargs)
    if retc != 0:
        print('Error making prv key')
        if verb and stderr:
            print(stderr)
        return not okay

    # Extract certificate (public) part
    cmd = f'/usr/bin/openssl x509 -outform der -in {kkey} -out {kcrt}'
    pargs = cmd.split()
    (retc, _stdout, stderr) = run_prog(pargs)
    if retc != 0:
        print('Error making crt')
        if verb and stderr:
            print(stderr)
        return not okay
    return okay


def make_new_keys(genkeys: GenKeysBase):
    """
    Set up before we use openssl to create_new_keys()
    Output:
        - signing_crt.crt - DER format Certificate
        - signing_prv.pem - private key (pem format)
        - signing_key.pem - privkey + cert in pem format
    """
    # pylint: disable=R0914
    if genkeys.verb:
        print('Making new keys ')

    now = date_time_now()
    now_str = now.strftime('%Y%m%d-%H%M')

    kdir = os.path.join(genkeys.cert_dir, now_str)
    os.makedirs(kdir, exist_ok=True)

    kvalid = '36500'
    kx509 = os.path.join(genkeys.cert_dir, 'x509.oot.genkey')
    kbasename = 'signing'
    kprv = os.path.join(kdir, kbasename + '_prv.pem')
    kkey = os.path.join(kdir, kbasename + '_key.pem')
    kcrt = os.path.join(kdir, kbasename + '_crt.crt')

    khash = genkeys.khash
    ktype = genkeys.ktype

    keyinfo = KeyInfo(kvalid, kx509, kprv, kkey, kcrt, khash, ktype)

    if not _create_new_keys(keyinfo, genkeys.verb):
        return False

    khash_file = os.path.join(kdir, 'khash')
    ktype_file = os.path.join(kdir, 'ktype')

    #
    # Put khash and ktype files in key dir.
    # The module signing script will read the hash/ktype
    #
    okay = True
    fobj = open_file(khash_file, 'w')
    if fobj:
        fobj.write(genkeys.khash + '\n')
        fobj.close()
    else:
        print(f'Failed to write: {khash_file}')
        okay = False

    fobj = open_file(ktype_file, 'w')
    if fobj:
        fobj.write(genkeys.ktype + '\n')
        fobj.close()
    else:
        print(f'Failed to write: {ktype_file}')
        okay = False

    #
    # update current link to new kdir
    # since the 'current' link and the actual keydir are in same dir we use
    # relative for link - safest in case certs-local is moved
    #
    if okay:
        link_temp = str(uuid.uuid4())
        link_temp = os.path.join(genkeys.cert_dir, link_temp)

        kdir_rel = os.path.basename(kdir)
        cur_link = os.path.join(genkeys.cert_dir, 'current')

        os.symlink(kdir_rel, link_temp)
        os.rename(link_temp, cur_link)

    return okay
