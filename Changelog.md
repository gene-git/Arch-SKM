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

