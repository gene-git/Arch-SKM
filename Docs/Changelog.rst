Changelog
=========

Tags
====

.. code-block:: text

	0.1.0 (2019-11-10) -> 5.0.2, origin/master (2026-02-06)
	117 commits.

Commits
=======


* 2026-02-06  : **5.0.2, origin/master**

.. code-block:: text

              - update Docs/Changelogs Docs/kernel-sign.pdf

* 2026-02-06  : **5.0.1**

.. code-block:: text

              - Update pkg-install script and README
 2026-02-05   ⋯

.. code-block:: text

              - update Docs/Changelogs Docs/kernel-sign.pdf

* 2026-02-05  : **5.0.0**

.. code-block:: text

                  - Version 5.0
            
                    * Preliminary support for ml-dsa-44, ml-dsa-65 and ml-dsa-87
            
                      These are the NIST approved post quantum compiting algorithms.
            
                      linux-next (as of 20260205) supports verifying signatures signed using ml-dsa-nn.
                      This version of kernel-sign will generate keys for those ml-dsa-nn algorithms
                      if specified in the kernel config.
            
                      We rely on the signing tool that is provided by the kernel itself to sign
                      any OOT kernel modules. Therefore, once the kernel tool supports signing
                      with ml-dsa, then we will too.
            
                    * Note: A future version may require the pyconcurrent module.
            
                      Its a lttle extra maintenance keeping duplicate code. For now,
                      we will use the pyconcurrent module if available otherwise we use a
                      local copy of the part we need.
            
                    * License updated to GPL version 2 or later.
            
                    * pkg-install update - byte compile python
            
                    * kernel-sign-update - remove unused code from certs-local/lib
 2025-06-26   ⋯

.. code-block:: text

              - update Docs/Changelogs Docs/kernel-sign.pdf

* 2025-06-26  : **4.4.0**

.. code-block:: text

              - If pyconcurrent module available use its run_prog() else use local copy.
 2025-06-22   ⋯

.. code-block:: text

              - update Docs/Changelogs Docs/kernel-sign.pdf

* 2025-06-22  : **4.3.0**

.. code-block:: text

              - run_prog: sync with latest from pyconcurrent
 2025-06-20   ⋯

.. code-block:: text

              - update Docs/Changelogs Docs/kernel-sign.pdf

* 2025-06-20  : **4.2.0**

.. code-block:: text

              - Pull local copy of latest run_prog from pyconcurrent
 2025-05-21   ⋯

.. code-block:: text

              - update Docs/Changelogs Docs/kernel-sign.pdf

* 2025-05-21  : **4.1.0**

.. code-block:: text

              - Use builtin types where possible. e.g. typing.List -> list
              - update Docs/Changelogs Docs/kernel-sign.pdf

* 2025-05-21  : **4.0.0**

.. code-block:: text

              - Tidy and Improve code:
                  PEP-8, PEP-257, PEP-484 PEP-561
                  Refactor
                Add tests : run pytest in the *tests* directory.
                  This will locate and use a kernel provided tool:
                  /usr/lib/modules/xxx/build/scripts/sign-file
 2024-12-31   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/kernel-sign.pdf

* 2024-12-31  : **3.0.2**

.. code-block:: text

              - Git tags are now signed.
                Update SPDX tags
 2023-11-05   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/kernel-sign.pdf

* 2023-11-05  : **3.0.1**

.. code-block:: text

              - fix readme.rst
              - update Docs/Changelog.rst Docs/kernel-sign.pdf

* 2023-11-05  : **3.0.0**

.. code-block:: text

                   - * key and hash types are now read from the kernel config file. Keeps everything consistent.
                     * Code re-org with supporing modules now moved to lib/xxx.py
                     * Confirm code works with hash type *sha3-512* introduced in kernel 6.7
                       Requires openssl 3.2+ / kernel 6.7+

* 2023-10-04  : **2.6.1**

.. code-block:: text

              - update Docs/Changelog.rst
              - Fix from Author: Expertcoderz <expertcoderzx@gmail.com>
              - Merge pull request #8 from Expertcoderz/patch-1
            
                Fix -v argument help text f-string
              - Fix -v argument help text f-string
 2023-09-27   ⋯

.. code-block:: text

              - update Docs/Changelog.rst

* 2023-09-27  : **2.6.0**

.. code-block:: text

              - Reorganize documrnts under Docs.
                Migrate to restructured text
                Now easy to build html and pdf docs using sphinx
 2023-03-31   ⋯

.. code-block:: text

              - update CHANGELOG.md

* 2023-03-31  : **2.5.1**

.. code-block:: text

              - update changelog
              - small README wordsmithing
 2023-03-30   ⋯

.. code-block:: text

              - update CHANGELOG.md

* 2023-03-30  : **2.5.0**

.. code-block:: text

              - Use Full path to openssl executable /usr/bin/openssl
 2023-01-06   ⋯

.. code-block:: text

              - Rename Changelog to CHANGELOG following our current release tools. Update

* 2023-01-06  : **2.4.0**

.. code-block:: text

              - Add SPDX licensing lines
                Update kernel doc reference link
 2022-07-07   ⋯

.. code-block:: text

              - Update kernel.org doc link to more recent kernel

* 2022-05-25  : **2.3.9**

.. code-block:: text

              - suppress a few silly pylint warnings

* 2022-05-21  : **2.3.8**

.. code-block:: text

              - Remove uneeded exception we just added. It is a subclass of OSError and so not needed.

* 2022-05-21  : **2.3.7**

.. code-block:: text

              - utils open_file catches (OSError,FileNotFoundError) exceoptions now

* 2022-05-18  : **2.3.6**

.. code-block:: text

              - update changelog
              - Fix open_file to only apply encoding to text files (thanks  pylint)

* 2022-05-18  : **2.3.5**

.. code-block:: text

               - - More tidy up - try keep pylint noise down so dont miss things it finds
              - delete old stuff
              - comment tweak

* 2022-05-18  : **2.3.4**

.. code-block:: text

              - Update Changelog
              - More code tidying in genkeys
              - little more tidyup - no functional changes
 2022-05-12   ⋯

.. code-block:: text

              - Add missing date to Changelog

* 2022-05-09  : **2.3.3**

.. code-block:: text

              - update Changelog
              - Use OSError exception which has replaced IOError
              - Catch OSError when file open fails

* 2022-05-08  : **2.3.2**

.. code-block:: text

              - Ack and Tested by by @itoffshore
              - update Changelog
              - trivial tidy

* 2022-05-08  : **2.3.1**

.. code-block:: text

              - more code tidying
              - Update Changelog
              - fix typo for refresh check
              - tidy and improve exception handling
              - tidy
              - more cleaning
              - more tidy
              - more tidy ups
              - some code tidying
              - another typo!
              - typo
              - fix file to name to avoid module conflict

* 2022-05-08  : **2.3.0**

.. code-block:: text

               - - Code re-org to be more robust and easier to read.
                 - Introduce KernelModSigner class and ModuleTool class to help organize
                 - Functionality is unchanged.

* 2022-05-04  : **2.2.1**

.. code-block:: text

              - Update Changelog and README to reflect sign_module.py replacing sign_manual.sh
              - Changelog - add date for 2.2.0

* 2022-05-04  : **2.2.0**

.. code-block:: text

              - update changelog
              - archive sign_manual.sh
              - turn off dev to ready for production
              - Improve module signing scripts:
                 - sign_module.py replaces sign_manual.sh
                 - dkms/kernel_sign.sh updated accordingly
                 - install-certs updated accordingly
                 - adds dependency : python-zstandard for handling zst compressed modules
 2022-05-03   ⋯

.. code-block:: text

              - README - small markdown tweaks

* 2022-05-03  : **2.1.1**

.. code-block:: text

              - update changelog
              - typo

* 2022-05-03  : **2.1.0**

.. code-block:: text

              - update Changelog
              - The key type and hash are now saved in files along side the keys. This allows the signing script to read them, and this means it no longer has hardcoded hash.  the sign script falls back on sha512 in case of previous key directory without a saved hash
 2022-05-02   ⋯

.. code-block:: text

              - remove extraneous |

* 2022-05-02  : **2.0.0**

.. code-block:: text

              - update changelog
              - word smith README
              - fix markdown on last addition

* 2022-05-02  : **1.3.5**

.. code-block:: text

              - Update README and Changelog
              - Add few more words about some available tooks by @itoffshore

* 2022-05-02  : **1.3.4**

.. code-block:: text

              - Update Changelog
              - White space patches from @itoffshore

* 2022-05-02  : **1.3.3**

.. code-block:: text

              - Update Changelog
              - Typo in echo found by @itoffshore
              - Changelog udpate
              - Add reference to @itoffshore aur package and github repo

* 2022-05-02  : **1.3.2**

.. code-block:: text

              - Fix hexdump typo "--e" to "-e"
              - Changelog update
              - Mindor markdown tweaks

* 2022-05-02  : **1.3.1**

.. code-block:: text

              - typo fix
              - Update Changelog

* 2022-05-02  : **1.3.0**

.. code-block:: text

              - Per @ittoffshore, add comment about quoting wildcard characters
              - Fixes from @itoffshore
                1. For manual signing
                   zstd modules use .zst instead of .zsrd
                   support for gzip
                2. For dkms
                   Add gzip support

* 2022-05-01  : **1.2.0**

.. code-block:: text

              - Expand help with reminder wildcards must be quoted

* 2022-05-01  : **1.1.0**

.. code-block:: text

              - tweak the prepare() example
              - small word smithing

* 2022-05-01  : **1.0.1**

.. code-block:: text

              - remove debugging

* 2022-05-01  : **1.0.0**

.. code-block:: text

              - Update readme and changelog
              - genkeys now handles multiple configs using shell glob with --config
              - support utilities
              - Rename tools to utils
              - Share coupld functions via tools.py
              - Add install-certs.py for use by package_headers() to simplify PKGBUILD
 2022-04-30   ⋯

.. code-block:: text

              - Update package_headers() to remove reference to file no longer being created. Part of issue #3
              - Add a little markdown to Changlelog.md
              - Update changes for 0.8.0 and 0.8.1

* 2022-04-30  : **0.8.1**

.. code-block:: text

              - Remove references to now unused scripts

* 2022-04-30  : **0.8.0**

.. code-block:: text

              - fix typo
              - Tidy up README
              - As per itoffshore check for key exists prior to getting mtime. Fixes bug in check_refresh()

* 2022-04-30  : **0.7.0**

.. code-block:: text

              - version [0.7.0]                                                     - 20220430
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

* 2021-10-20  : **0.4.0**

.. code-block:: text

              - Update kernel-sign.sh for compressed modules

* 2019-11-15  : **0.3.0**

.. code-block:: text

              - Tidy Readme

* 2019-11-10  : **0.2.0**

.. code-block:: text

              - tidy up readme

* 2019-11-10  : **0.1.0**

.. code-block:: text

              - Initial revision


