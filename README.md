
# OVERVIEW 

Signed kernel modules provide a mechanism for the kernel to verify the integrity of a module.
This provides the tools needed to build a kernel with support for signed modules.

## Contents

    1. Introduction
    2. How to sign kernel modules using a custom kernel
    3. Summary of what needs to be done
    4. Kernel configuration
        1. Kernel command line
    5. Tools needed
        1. kernel build package
        2. dkms support
    6. Modify PKGBUILD
        1. prepare()
        2. _package-headers()
    7. Files Required
        1. certs-local/genkeys.py
        2. certs-local/x509.oot.genkey
        3. certs-local/install-certs.py
        4. certs-local/sign_manual.sh
        5. certs-local/dkms/kernel-sign.conf
        6. certs-local/dkms/kernel-sign.sh
    8.  Arch AUR package

### See:

 - [Arch Wiki on signed kernel modules](https://wiki.archlinux.org/title/Signed_kernel_modules)
 - [Kernel Docs on module signing](https://www.kernel.org/doc/html/v5.18-rc4/admin-guide/module-signing.html)

# 1. Introduction                                     |

The Linux kernel distinguishes and keeps separate the verification of modules from requiring or 
forcing modules to verify before allowing them to be loaded. Kernel modules fall into 2 classes:

Standard "in tree" modules which come with the kernel source code. They are compiled during the 
normal kernel build.

Out of tree modules which are not part of the kernel source distribution. They are built outside 
of the kernel tree, requiring the kernel headers package for each kernel they are to be built for. 
They can be built manually for a specific kernel and packaged, or they can be built whenever 
needed using DKMS <https://wiki.archlinux.org/index.php/DKMS>. 

Examples of such packages, provided by Arch, include:

  - virtualbox-guest-modules-arch <https://www.archlinux.org/packages/?name=virtualbox-guest-modules-arch> 

During a standard kernel compilation, the kernel build tools create a private/public key pair and 
sign every in tree module (using the private key). The public key is saved in the kernel itself. 
When a module is subsequently loaded, the public key can then be used to verify that the module 
is unchanged.

The kernel can be enabled to always verify modules and report any failures to standard logs. 
The choice to permit the loading and use of a module which could not be verified can be either 
compiled into kernel or turned on at run time using a kernel parameter as explained below.
(https://wiki.archlinux.org/index.php/Kernel_parameter)

# 2. How to sign kernel modules using a custom kernel  

The starting point is based on a custom kernel package as outlined in this article Kernel/Arch Build System. 
<https://wiki.archlinux.org/index.php/Kernel/Arch_Build_System>

We will modify the build to:

  - Sign the standard in tree kernel modules
  - Provide what is needed to have signed out of tree modules and for the kernel to verify those modules.

Note: The goal here is to have:

  - In tree modules signed during the standard kernel build process.
    The standard kernel build creates a fresh public/private key pair on each build.

  - Out of tree modules are signed and the associated public key is compiled in to the kernel.
    We will create a separate public/private key pair on each build.

#     3. Summary of what needs to be done 

Each kernel build needs to made aware of the key/cert being used. Fresh keys are 
generated with each new kernel build.

A kernel config parameter is now used to make kernel aware of additional signing key: 

  CONFIG_SYSTEM_TRUSTED_KEYS="/path/to/oot-signing_keys.pem".

Keys and signing tools will be stored in current module build directory. Nothing needs to be done to 
clean this as removal is handled by the standard module cleanup. Certs are thus 
installed in /usr/lib/modules/<kernel-vers>-<build>/certs-local.  

#     4. Kernel configuration  

CONFIG_SYSTEM_TRUSTED_KEYS will be added automatically as explained below. 
In addition the following config options should be set by either manually editing the 
'config' file, or via make menuconfig in the linux 'src' area and subsequently copying 
the updated '.config' file back to the build file 'config'.  It is preferable to use elliptic curve type keys and zstd compression. 

  - CONFIG_MODULE_SIG=y
    Enable Loadable module suppot --->
    Module Signature Verification           -  activate

  - CONFIG_MODULE_SIG_FORCE=n
    Require modules to be validly signed -> leave off

        This allows the decision to enforce verified modules only as boot command line.
        If you are comfortable all is working then by all means change this to 'y'
        Command line version of this is : module.sig_enforce=1

  - CONFIG_MODULE_SIG_HASH=sha512
    Automatically sign all modules  - activate
    Which hash algorithm    -> SHA-512

  - CONFIG_MODULE_COMPRESS_ZSTD=y
    Compress modules on installation        - activate
        Compression algorithm (ZSTD)

  - CONFIG_MODULE_SIG_KEY_TYPE_ECDSA=y
    Cryptographic API --->
        Certificates for Signature Checking --->
            Type of module signing key to be generated -> ECDSA

  - CONFIG_MODULE_ALLOW_MISSING_NAMESPACE_IMPORTS=n
    Enable Loadable module support --->
        Allow loading of modules with missing namespace imports -> set off 

## 4.1 Kernel command line 

  After you are comfortable things are working well you can enable the kernel parameter to 
  require that the kernel only permit verified modules to be loaded:

    module.sig_enforce=1

# 5. Tools needed 

## 5.1 kernel build package 

  In the directory where the kernel package is built:

  $ mkdir certs-local

  This directory will provide the tools to create the keys, as well as signing kernel modules.

  Put these files into certs-local:

    genkeys.py
    x509.oot.genkey
    install-certs.py
    sign_manual.sh

  The files genkey.py and its config x509.oot.genkey are used to create key pairs.
  It also provides the kernel with the key to sign the out of tree modules by updating the config file 
  used to build the kernel.

  The sign_manual script is used to sign out of tree kernel modules by hand.

  genkeys.py will create the key pairs in a directory named by date-time. It defaults to refreshing
  the keys every 7 days but this can be changed with command line option.

  It also creates a soft link named 'current' which points to the newly created directory with the 'current' keys.
  The actual key directory is named by date and time.

  genkeys will check and update kernel configs given by the  --config config(s) option. This takes either a single
  config file, or a shell glob for mulitple files. e.g. --config 'conf/config.*'. Remember to quote any wildcard 
  characters to prevent the shell from expanding them. 
 
  All configs will be updated with the same key. The default keytype is ec (elliptic curve) and the default
  hash is sha512. These can be changed with command line options. See genkeys.py -h for more details.

  install-certs.py is to be called from the package_headers() function of PKGBUILD to install the signing keys. Example is given below. 
  
  These files are all provided.

  ## 5.2 dkms support

  $ mkdir certs-local/dkms

  Add 2 files to the dkms dir:

    kernel-sign.conf
    kernel-sign.sh

  These will be installed in /etc/dkms and provide a mechanism for dkms to automatically sign 
  modules (using the local key above) - this is the reccommended way to sign kernel modules. 
  As explained, below - once this is installed - all that is needed to have dkms automatically 
  sign modules is to make a soft link:

    $ cd /etc/dkms
    ln -s kernel-sign.conf <module-name>.conf

  For example:

    ln -s kernel-sign.conf vboxdrv.conf

  The link creation can easily be added to an arch package to simplify further if desired.

# 6. Modify PKGBUILD 

We need to make changes to kernel build as follows:

## 6.1 prepare()

  Add the following to the top of the prepare() function:

    prepare() {

        msg2 "Rebuilding local signing key..."
        # adjust cerdir as needed 
        certdir='../certs-local'
        $certdir/genkeys.py -v --config ../config
      ... 
    }

The default key regeneration refresh period is 7 days, but this can be changed on the command line. So if you want to create new keys monthly, then add "--refresh 30days" as an argument to genekeys.py. You can refresh on every build by using "--refresh always". Refresh units can be seconds,minutes,hours,days or weeks. 

## 6.2 _package-headers() 

  Add the following to the bottom of the _package-headers() function:

    _package-headers() {

    ...

    #
    # Out of Tree Module signing
    # This is run in the kernel source / build directory
    #
    msg2 "Local Signing certs for out of tree modules..."
      
    certs_local_src="../../certs-local" 
    certs_local_dst="${builddir}/certs-local"

    ${certs_local_src}/install-certs.py $certs_local_dst

    # install dkms tools if needed
    dkms_src="$certs_local_src/dkms"
    dkms_dst="${pkgdir}/etc/dkms"
    mkdir -p $dkms_dst

    rsync -a $dkms_src/{kernel-sign.conf,kernel-sign.sh} $dkms_dst/
    }

# 7. Files Required 

These are the supporting files referenced above. Do not forget to make the scripts executable.

  - certs-local/genkeys.py
  - certs-local/install-certs.py
  - certs-local/x509.oot.genkey
  - certs-local/sign_manual.sh
  - certs-local/dkms/kernel-sign.conf
  - certs-local/dkms/kernel-sign.sh


# 8. Arch AUR packags

 - There is alos a package in AUR [Arch Sign Modules](https://aur.archlinux.org/packages/arch-sign-modules) and its github repo [Arch-SKM](https://github.com/itoffshore/Arch-SKM)
