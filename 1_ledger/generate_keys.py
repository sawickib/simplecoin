#!/usr/bin/env python3

import Crypto
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256

keys = RSA.generate(1024)
pubkey = keys.publickey()
pktxt = pubkey.exportKey()

h = SHA256.new(pktxt)
ht = h.hexdigest()[:4]

with open(ht+"_priv.pem", "wb") as file:
    file.write(keys.exportKey(passphrase='abc'))
    print("Private RSA key saved to "+ht+"_priv.pem")
    
with open(ht+"_pub.pem", "wb") as file:
    file.write(pktxt)
    print("Public RSA key saved to "+ht+"_pub.pem")
