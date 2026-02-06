###########
kernel-sign
###########

Overview
========

Signed kernel modules allow the kernel to verify the integrity of a module before loading it.
This package provides the tools and information needed to build a kernel that supports signed 
*out of tree* (OOT) modules. An OOT module is any kernel module that is not 
part of the upstream Linux kernel itself.

Note that all git tags are signed with arch@sapience.com key which is available via WKD
or for download from https://www.sapience.com/tech.

Latest Changes
--------------

**Version 5.0**

* Preliminary support for **ml-dsa-44**, **ml-dsa-65** and **ml-dsa-87**

  These are the NIST approved post quantum computing algorithms.

  linux-next (as of 20260205) supports verifying signatures signed using ml-dsa-nn.
  This version of *kernel-sign* will generate keys for those ml-dsa-nn algorithms 
  if specified in the kernel config.

  We rely on the signing tool that is provided by the kernel itself to sign 
  any OOT kernel modules. Therefore, once the kernel tool supports signing
  with ml-dsa, then we will too.

* Note: A future version may require the *pyconcurrent* module.

  Its a lttle extra maintenance keeping duplicate code. For now,
  we will use the pyconcurrent module if available otherwise we use a
  local copy of the part we need.

* License updated to GPL version 2 or later.

* pkg-install script updated.

  Byte compile the python code and remove any no-longer needed files.


Where to get Kernel-Sign 
========================

Kernel-Sign is available in the Github repo:

* `Kernel_Sign`_ - This is the current version and includes the documentation pdf file.

Also see:

* `Kernel Docs`_  - upstream kernel documentation on module signing.
* `Arch Wiki`_  - this may not always be up to date.


############
Introduction 
############

Kernel Modules
==============

Linux kernel module verification can be made a requirement, thereby 
forcing modules to be verified before allowing them to be loaded. 

At a high level there are 2 classes of Kernel modules:

Standard **in tree** modules: these come with the kernel source code and are compiled during a 
normal kernel build.

**Out of tree** (OOT) modules: thse are not part of the kernel source and are built outside 
of the kernel tree. They require the kernel headers for each kernel they are built for. 
They can be built manually for a specific kernel and packaged, or they can be built whenever 
needed by using dynamic kernel module support (DKMS) `DKMS`_ 

Some examples of such modules include:

* `Virtual Box <https://www.archlinux.org/packages/?name=virtualbox-guest-modules-arch>`_ guest modules.
* `ZFS File System <https://wiki.archlinux.org/title/ZFS>`_ modules.
* `Nvidia Propietry Driver <https://wiki.archlinux.org/title/NVIDIA>`_ modules.
    
During a standard kernel compilation, the kernel build tools create a private/public key pair and 
sign every in tree module (using the private key). The public key is saved in the kernel itself. 
When a module is subsequently loaded, the public key can then be used to verify that the module 
is unchanged.

The kernel can be enabled to always verify modules and report any failures to standard logs. 
The choice to permit the loading and use of a module which could not be verified can be either 
compiled into kernel or turned on at run time using a kernel parameter as explained 
in Arch Wiki Kernel Parameters `Arch Wiki Kernel Parameters`_.


How to sign kernel modules using a custom kernel  
================================================

The starting point is based on building a custom kernel package outlined in 
Kernel/Arch Build System `Kernel/Arch Build System`_,

We will adjust the build to:

* Sign the standard in tree kernel modules
* Provide what is needed to have signed out of tree modules and for the kernel to verify those modules.

Note: The goal is to have:

* In tree modules signed during the standard kernel build process.

  The standard kernel build creates a fresh public/private key pair on each build.

* Out of tree modules are signed using separate private key
 
  The OOT companion public key is made available to the kernel.
  We will create a separate public/private key pair on each build.

Summary of what needs to be done 
================================

Each kernel build needs to made aware of the key/cert being used. Fresh keys are 
generated with each new kernel build.

A kernel config parameter is now used to make kernel aware of additional signing key::

  CONFIG_SYSTEM_TRUSTED_KEYS="/path/to/oot-signing_keys.pem".

Keys and signing tools will be stored in current module build directory. Nothing needs to be done to 
clean this as removal is handled by the standard module cleanup. 

Certs are thus installed in::

    /usr/lib/modules/<kernel-vers>-<build>/certs-local.  

####################
Kernel configuration  
####################

Kernel Config File
==================

CONFIG_SYSTEM_TRUSTED_KEYS will be added automatically as explained below. 
In addition the following config options should be set by either manually editing the 
'config' file, or via make menuconfig in the linux 'src' area and subsequently copying 
the updated *.config* file back to the build file *config*.  
It is preferable to use elliptic curve type keys and zstd compression. 

* CONFIG_MODULE_SIG=y

  Enable Loadable module suppot --->

  Module Signature Verification ->  activate

* CONFIG_MODULE_SIG_FORCE=n

  Require modules to be validly signed -> leave off

  This allows the decision to enforce verified modules only as boot command line.
  If you are comfortable all is working then by all means change this to 'y'
  Command line version of this is : module.sig_enforce=1

* CONFIG_MODULE_SIG_HASH=sha512

  Automatically sign all modules  -> activate
  Which hash algorithm    -> SHA-512

  kernel 6.7 and later support sha3 hashes. The preferred hash choice is then
  sha3-512. This also requires openssl version 3.2 or newer.


* CONFIG_MODULE_COMPRESS_ZSTD=y

  Compress modules on installation -> activate
  Compression algorithm (ZSTD)

* CONFIG_MODULE_SIG_KEY_TYPE_ECDSA=y

  Cryptographic API --->
  Certificates for Signature Checking --->
  Type of module signing key to be generated -> ECDSA

* CONFIG_MODULE_ALLOW_MISSING_NAMESPACE_IMPORTS=n

  Enable Loadable module support --->
  Allow loading of modules with missing namespace imports -> set off 

Kernel command line 
===================

After you are comfortable things are working well you can enable the kernel parameter to 
require that the kernel only permit verified modules to be loaded:

.. code-block:: bash

    module.sig_enforce=1

############
Installation 
############

kernel build package 
====================

Use the *pkg-install* script from the repo to install *kernel-sign*. 

The script takes one optional argument, which is the destination directory
where the source is to be installed. 
If script is run by root, then the destinaion defaults to **/**.

.. code-block:: bash

   ./pkg-install

This installs the source files and documentation into */usr/src/kernel-sign*. 
and *dkms* helper tools into */etc/dkms*


Building Kernel
===============

After *kernel-sign* is installed it can now be used during kernel builds.
There are 3 things needed in the PKGBUILD to support signed kernel modules.

* Having a copy of *certs-local* in the same directory as the kernel PKGBUILD

  This has tools and the keys used to sign the modules.

* Generate new keys periodcally.

To achieve these 2 items, edit the PKGBUILD and add this to the *prepare()* function:

.. code-block:: bash

   echo "Gewnerate OOT Modules signing keys ..."
   /usr/src/kernel-sign/kernel-sign-update
   ./certs-local/genkeys.py -v --config ./config --refresh 30d


*kernel-sign-update* makes a copy of *certs-local* from the source */usr/src/kernel-sign* and 
ensures that it is kept up to date.

*config* is the usual kernel config file and is used generate new signing keys 
every 30 days. The hash and key types are taken from the kernel config this
ensures that the hash and key algos are used to sign in-tree modules are 
also used to sign the OOT modules. The OOT modules ure signed with a 
separate signing key.

The 3rd item is:

* Install the OOT certs into the kernel build directory:

  At the end of the _package-headers() function add:

  
.. code-block:: bash

    echo "Install OOT Modules Signing certs ..."
    certs_local_src="$startdir/certs-local"
    certs_local_dst="${builddir}/certs-local"
    $certs_local_src/install-certs.py $certs_local_dst

The kernel will use the certificate (public key) to validate signed OOT modules.
The certs are installed into */usr/lib/modules/<kernel-version>/build/certs-local/*.

When the kernel package is built, it will now have all the tools, keys and certs required
for OOT module signing.

The last item is to use these to sign any OOT modules which is discussed below in the
`Signing with DKMS`_ section.

More Details
============

genkeys.py
----------

genkeys.py reads the file *x509.oot.genkey* to create key pairs. This is similar
to how the in-tree modules work.

It also updates the config file with the OOT signing key information so that the 
kernel can verify signed OOT modules.

Key pairs are created in a directory named by date-time. It defaults to refreshing
the keys every 7 days but this can be changed with the *--refresh* command line option.

It also creates a symlink named 'current' that points to the newly created directory with 
the 'current' keys.

It checks and updates kernel configs given by the *--config config(s)* option. This can be either a single
config file, or a shell glob for mulitple files. e.g. *--config 'conf/config.*'*. Remember to quote any wildcard 
characters to prevent the shell from expanding them. 
 
All configs will be updated with the same key. The default keytype and hash are taken from 
the kernel config (CONFIG_MODULE_SIG_HASH and CONFIG_MODULE_SIG_KEY_TYPE_xxx).

If multiple kernel configs are being used, they must all use same key and hash types.

sign_module.py 
--------------

This tool signs out of tree kernel modules. It can be run manually but is typically invoked 
from */etc/dkms/kernel-sign.sh*. 

It can handle uncompressed modules as well as those compressed with zstd, xz or gzip.
It depends on python-zstandard package to do so.

install-certs.py
----------------

This is called from the package_headers() function of PKGBUILD to install the signing keys. 
Example is given below. 
  
These files are all provided.

Signing with DKMS
===========-----=

**Important**

DKMS a mechanism for out-of-tree modules to be compiled against the kernel headers.
It is one thing to use signed modules provided in the kernel source but it is quite 
another to use modules, signed or not, that are out-of-tree. Any such module will
*taint* the kernel. See kernel docs `tainted_kernel`_ for more information.

The tools installed in /etc/dkms provide the mechanism for dkms to automatically sign 
modules using the local keys discussed above. 

This is the reccommended way to sign OOT kernel modules. 
All that is needed for dkms to automatically sign modules is to make a soft link:

.. code-block:: bash

        cd /etc/dkms
        ln -s kernel-sign.conf <module-name>.conf

For example:

.. code-block:: bash

        ln -s kernel-sign.conf vboxdrv.conf

The link creation can easily be added to an arch package to simplify further if desired.


##############
Required Files
##############

This is a list of the required files installed in *certs-local*:

* genkeys.py
* install-certs.py
* sign_module.py
* x509.oot.genkey
* lib/class_genkeys.py
* lib/_genkeys_base.py
* lib/get_key_hash.py
* lib/__init__.py
* lib/make_keys.py
* lib/refresh_needed.py
* lib/run_prog_copy.py
* lib/run_prog_local.py
* lib/signer_class.py
* lib/update_config.py
* lib/utils.py

And those in */etc/dkms*:

* kernel-sign.sh
* kernel-sign.conf

################
Arch AUR packags
################

AUR Packages
============

There is an `Arch Sign Modules`_ package in the AUR along with
its companion github repo `Arch-SKM`_ which make use of `Kernel_Sign`_

arch-sign-modules reduces the manual steps for building a fully signed custom 
kernel to 3 commands to *Update*, *Build* and *Install* a kernel.

.. code-block:: bash

    abk -u kernel-name
    abk -b kernel-name
    abk -i kernel-name

For more information see `Arch-SKM-README`_ and example `Arch-SKM-PKGBUIILD`_

.. _`Arch-SKM`: ](https://github.com/itoffshore/Arch-SKM) 
.. _`Arch Sign Modules`: https://aur.archlinux.org/packages/arch-sign-modules 
.. _`Arch-SKM-README`:  https://github.com/itoffshore/Arch-SKM/blob/master/README.scripts.md
.. _`Arch-SKM-PKGBUIILD`: https://github.com/itoffshore/Arch-SKM/blob/master/Arch-Linux-PKGBUILD-example


#############
Older Changes
#############

* Tidy and Improve code:

  * PEP-8, PEP-257, PEP-484 PEP-561
  * Refactor

 * Add tests : run pytest in the *tests* directory.
   
   This will locate and use a kernel provided tool:
   /usr/lib/modules/xxx/build/scripts/sign-file

 * key and hash types are now read from the kernel config file. Keeps everything consistent.
 * Code re-org with supporing modules now moved to lib/xxx.py
 * Code works with hash type sha3-xxx (e.g. *sha3-512*) available in kernel 6.7 and openssl 3.2 or later.

.. _`Kernel_Sign`: https://github.com/gene-git/arch-skm
.. _`Arch Wiki`: https://wiki.archlinux.org/title/Signed_kernel_modules
.. _`Kernel Docs`: https://docs.kernel.org/admin-guide/module-signing.html
.. _`DKMS`: https://wiki.archlinux.org/index.php/DKMS). 
.. _`Arch Wiki Kernel Parameters`: https://wiki.archlinux.org/index.php/Kernel_parameters
.. _`Kernel/Arch Build System`: https://wiki.archlinux.org/index.php/Kernel/Arch_Build_System
.. _`tainted_kernel`: https://docs.kernel.org/admin-guide/tainted-kernels.html
