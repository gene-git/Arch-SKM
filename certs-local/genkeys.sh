#!/bin/bash
#
# Create new pub/priv key pair for signing out of tree kernel modules.
#
# Each key pair is stored by date-time
#
# Gene 20191110

Dt=$(date +'%Y%m%d-%H%M')

mkdir -p $Dt

KernKey="${Dt}/signing_key.pem"
PrivKey="${Dt}/signing_prv.key"
KernCrt="${Dt}/signing_crt.crt"


openssl req -new -nodes -utf8 -sha512 -days 36500 -batch -x509 -config ./x509.oot.genkey \
        -outform PEM -out $KernKey -keyout $KernKey


chmod 0600 $KernKey
openssl pkey -in $KernKey -out $PrivKey
openssl x509 -outform der -in $KernKey -out $KernCrt

rm -f current; ln -s $Dt current

rm -f current_key_dir
echo "$Dt" > ./current_key_dir

exit 0
