version [0.8.1]                                                     - 20220430
  - Remove references to now unused scripts

version [0.8.0]                                                     - 20220430
  - Fix Issue #2 on github 
    Per itoffshore check for key exists prior to getting mtime. Fixes bug in check_refresh(
  - Tidy up README
  - fix typo

version [0.7.0]                                                     - 20220430
  - Add genkeys.py (replaces both genkeys.sh and fix_config.sh) 
    This supports refresh key frequency (default is 7 days) 
    PKGBUILD use: ./genkeys.py -v
    Creates new keys as needed and updates kernel config.

version [0.6.0]                                                     - 20220430
  - Support zstd module compression in sign_manual.sh
  - Improve hexdump for signed module detection in sign_manual.sh
  - Has hardcoded sha512 hash - needs updating/replacing

version [0.5.0]                                                     - 20220420
  - Switch to using elliptic curve 

version [0.4.0]                                                     - 20221021
  - Update kernel-sign.sh to handle compressed modules

Version [0.3.0]                                                     - 20191115
  - TIdy up Readme

Version [0.2.0]                                                     - 20191110
  - TIdy up Readme

Version [0.1.0]                                                     - 20191110
  - Initial version

