#!/usr/bin/python
# 
# -------------------------
#   class KernelModSigner 
#       Handles signing, keys etc.
# -------------------------
#   class ModuleTool
#       uses KernelModSigner 
#       For one module: read/write/compress/decompress and sign 
# -------------------------
#
# Handle the actual signing of one kernel module
#
#  Modules can be uncompressed (.ko) or compressed with zstd (.zst), xz (.xz) or gzip (.gz)
#  Modules may also be already signed in which case the signature is stripped out before re-signing.
#  
#  NB - stripping removes all debug info including signature.
#
#  Notes:
#  --------
#  get_kernel_signer()
#
#  sign_module.py is installed in each kernel build directory under certs-local.
#  So, this uses that to locate the kernel build dir and hence the kernel (compiled) signing tool
#
#  i.e.
#      me = '/usr/lib/modules/<kern-vers>/build/certs-local/sign_module.py'
#      signer = /usr/lib/modules/<kern-vers>/build/scripts/sign-file
#
#  key files reside in current dir:
#      /usr/lib/modules/<kern-vers>/build/certs-local/current/
#      signing_key.pem , signing_crt.crt, khash
#
# We use file extension to determine if/how compressed. We do not use magic bytes
# We work in memory rather than via filesystem - each module is small emough its not a problem
#
# While it may be fine to leave existing sig and sign the (previously) signed module - we choose to 
# strip it. Maybe simpler and cleaner not to bother - not clear if this may cause problem for
# kernel sig check or not. So we strip it out. This also removes any debug symbols so it has a different
# downside if the module had any.
#
# Gene - 2022-0508
#
import os
import sys

import zstandard
import lzma
import gzip
import uuid
import utils

# -------------------------------------------------------------------------------------------
class KernelModSigner:

    """
     kernelModISigner class handles key management and signing of kernel modules
     Once instantiated use to sign module(s)
     Public methods: sign_module()
    """

    def __init__(self, me):
        self.signer = None
        self.key = None
        self.crt = None
        self.khash = None
        self.initialized = None
        #
        # extract kernel directory from me which is the full path to calling executable 
        # Provides path to kernel signer and to keys
        #
        my_path = os.path.realpath(me)
        my_dir = os.path.dirname(my_path)
        build_dir = os.path.dirname(my_dir)

        # signing executable and keys
        self.signer = os.path.join(build_dir, 'scripts/sign-file')
        self.key = os.path.join(my_dir, 'current/signing_key.pem')
        self.crt = os.path.join(my_dir, 'current/signing_crt.crt')
        khash_file = os.path.join(my_dir, 'current/khash')

        # missing khash - temp backward compat only - remove at some point
        if os.path.exists(khash_file) :
            fp = open(khash_file, 'r')
            if fp:
                khash = fp.read()
                khash = khash.strip()
                fp.close()
            else:
                khash = 'sha512'
        else:
            khash = 'sha512'
        self.khash = khash

        if not os.path.exists(self.key) :
            print ('Missing key file : ' + self.key)
            self.key = None
            if not os.path.exists(self.crt) :
                self.crt = None
                print ('Missing crt file : ' + self.crt)
        else:
            self.initialized = True

    # 
    # Does actual module signing Using key_info 
    #
    def sign_module(self, mod_path):

        pargs = [self.signer, self.khash, self.key, self.crt, mod_path] 
        [rc, sout, serr] = utils.run_prog(pargs)
        if rc != 0:
            print ('Signing failed')
        return rc

# -------------------------------------------------------------------------------------------
# Class ModuleTool
#
# Methods to compress / decompress, check for existing signature, remove existing signature
# Uses KernelModSigner class for key managemen and signing.
# 
# When checking for sig we minimize the search by looking in last few bytes - say last x bytes
#                 <- x -> 
#   [0]------[N-x]-------[N-1]
# 
#  => N-x > x
#
class ModuleTool:
    """
     Class ModuleTool
     Tools to decompress, recompress and check and remove existing signature, sign module file
     Public methods: read() and sign()
    """

    def __init__ (self, signer, mod_path):
        self.signer = signer
        self.data = None
        self.compress = None
        self.signed = None
        self.mod_path = None
        self.mod_dir = None
        self.fpath = None
        self.fext = None
        self.path_ok = False

        path_exists = os.path.exists(mod_path) 
        if path_exists and os.path.isfile(mod_path):
            self.mod_path = os.path.abspath(mod_path)
            self.mod_dir = os.path.dirname(self.mod_path)

            (self.fpath, self.fext) = os.path.splitext(self.mod_path)
            known_ext = ['.ko', '.zst', '.xz', '.gz']
            if self.fext in known_ext:
                self.path_ok = True
            else:
                print ('Unkown extension : ' + self.fext)
        else:
            print ('Bad Module file: ' + mod_path) 

    def strip_sig(self, mod_path):
        pargs =  ['/usr/bin/strip', '--strip-debug', mod_path]
        [rc, output, errors] = utils.run_prog(pargs)
        return rc

    def is_signed(self):
        if self.signed:
            return self.signed

        sign_flag = b'Module signature'
        chunk = 100
        size = len(self.data)
        b0 = 0
        b1 = size-1
        if size - chunk >= chunk:
            b0 = size - chunk 
        found = self.data.find(sign_flag, b0, b1) 
        if found >= 0:
            self.signed = True
        return self.signed

    def read (self):
        if self.data:
            return self.data
        fp = open(self.mod_path, 'rb')
        if fp:
            raw_data = fp.read()
            fp.close()
        else:
            print('Failed to read : ' + self.mod_path)
            return None

        # decompress if needed - allowed extensions pre-validated in init()
        match self.fext:
            case '.ko':
                self.data = raw_data
                self.compress = False
            case '.zst' :
                dctx = zstandard.ZstdDecompressor()
                self.data = dctx.decompress(raw_data)
                self.compress = True
            case '.xz' :
                self.data = lzma.decompress(raw_data)
                self.compress = True
            case  '.gz' :
                self.data = gzip.decompress(raw_data)
                self.compress = True
        return self.data

    def sign(self):
        """
         sign temp file, compress if needed  and rename to orig. 
        """
        ok = True
        data = self.read()
        if not data:
            return not ok

        ftmp = str(uuid.uuid4())
        ptmp = os.path.join(self.mod_dir, ftmp) 
        fp = open(ptmp, 'wb')
        if fp:
            fp.write(data)
            fp.close()
        else:
            print('Failed to create temp mod file')
            return not ok

        if self.is_signed():
            ret = self.strip_sig(ptmp)
            if ret != 0:
                print ('Failed to strip temp file')
                utils.remove_file(ptmp)
                return not ok
        
        ret = self.signer.sign_module(ptmp)
        if ret != 0:
            utils.remove_file(ptmp)
            return not ok

        if self.compress:
            fp =  open(ptmp, 'rb')
            raw_data = fp.read()
            fp.close()

            match self.fext:
                case '.zst' :
                    cctx = zstandard.ZstdCompressor()
                    mod_data = cctx.compress(raw_data)
                case '.xz' :
                    mod_data = lzma.compress(raw_data)
                case  '.gz' :
                    mod_data = gzip.compress(raw_data)
            fp = open(ptmp, 'wb')
            if fp:
                fp.write(mod_data)
                fp.close()
            else:
                print ('Failed to write compressed temp file: ' + ptmp)
                utils.remove_file(ptmp)
                return not ok
        os.rename (ptmp, self.mod_path)
        return ok

