
### version [2.2.0] 20220504

 - Improve module signing scripts.
 - sign_module.py replaces sign_manual.sh
 - dkms/kernel_sign.sh updated accordingly
 - install-certs updated accordingly
 - adds dependency : python-zstandard for handling zst compressed modules

### version [2.1.1] 20220503

 - Bah, typo

### version [2.1.0] 20220503

 - The key type and hash are now saved in files along side the keys. 
   This allows the signing script to read them, and means it no longer has hardcoded hash.  
   The sign script falls back on sha512 in case (older) key directory has no saved hash file

### version [2.0.0] 20220502

 - Significant recent changes warrant a major version bump.

### version [1.3.5] 20220502

 - Typo in README
 - Add some more info about tools availabe by @itoffshore leveraging Arch-SKM.

### version [1.3.4] 20220502

 - Apply whitespace patches from @itoffshore

### version [1.3.3] 20220502

 - Add reference to @itoffshore aur package and github repo
 - Typo in echo found by @itoffshore

### version [1.3.2] 20220502

 - Fix hexdump typo "--e" to "-e"

### version [1.3.1] 20220502

 - Typo

### version [1.3.0] 20220501

 - Fixes from @itoffshore
    1. For manual signing
       zstd modules use .zst instead of .zstd
       Add support for gzip
    2. For dkms
       Add gzip support
 - Update README with comment about quoting wildcard characters

### version [1.2.0] 20220501

 - Expand help with reminder wildcards must be quoted

### version [1.1.0] 20220501

 - Tweak the prepare() example
 - Word smithing

### version [1.0.1] 20220501

 - Turn off debug

### version [1.0.0] 20220501

 - Provide install-certs.py to simplfy PKGBUILD
 - Enhance genkeys:
     - Can be run from any directory, but must reside in certs-local
     - Defaults to elliptic curve and sha512 hash. Can be overriden on command line.
     - Accepts one or multiple config files to be updated with same key. 
       Provide config file(s) using shell globs. E.g
       genkeys.py --config 'confdir/config.*'

### version [0.8.1] 20220430

  - Remove references to now unused scripts

### version [0.8.0] 20220430

  - Fix Issue #2 on github 
    Per itoffshore check for key exists prior to getting mtime. Fixes bug in check_refresh(
  - Tidy up README
  - fix typo

### version [0.7.0] 20220430

  - Add genkeys.py (replaces both genkeys.sh and fix_config.sh) 
    This supports refresh key frequency (default is 7 days) 
    PKGBUILD use: ./genkeys.py -v
    Creates new keys as needed and updates kernel config.

### version [0.6.0] 20220430

  - Support zstd module compression in sign_manual.sh
  - Improve hexdump for signed module detection in sign_manual.sh
  - Has hardcoded sha512 hash - needs updating/replacing

### version [0.5.0] 20220420

  - Switch to using elliptic curve 

### version [0.4.0] 20221021

  - Update kernel-sign.sh to handle compressed modules

### Version [0.3.0] 20191115

  - Tidy up Readme

### Version [0.2.0] 20191110

  - TIdy up Readme

### Version [0.1.0] 20191110

  - Initial version

