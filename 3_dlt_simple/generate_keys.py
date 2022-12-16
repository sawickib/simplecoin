#!/usr/bin/env python3

import Crypto
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import sys

keys = RSA.generate(1024)
pubkey = keys.publickey()
pktxt = pubkey.exportKey()

h = SHA256.new(pktxt)
name = sys.argv[1]

with open(name+"_priv.pem", "wb") as file:
    file.write(keys.exportKey(passphrase='abc'))
    print("Private RSA key saved to "+name+"_priv.pem")
    
with open(name+"_pub.pem", "wb") as file:
    file.write(pktxt)
    print("Public RSA key saved to "+name+"_pub.pem")
