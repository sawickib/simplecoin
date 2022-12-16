#!/usr/bin/env python3

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
import json

sender = "16b5"
receiver = "3e43"
amount = 102

##############
# Sign JSON transaction

with open("keys/"+sender+"_priv.pem", "rb") as file:
    try:
        keys=RSA.importKey(file.read(), passphrase='abc')
    except ValueError:
        print("ERROR: Failed to load RSA keys")
    file.close()

transaction = {"sender":sender, "receiver":receiver, "amount":amount}
msg = json.dumps(transaction, sort_keys=True)
h = SHA256.new(msg.encode('UTF-8'))
s = pkcs1_15.new(keys).sign(h)

signed_transaction = {'transaction': transaction, 'signature': s.hex()}

print(json.dumps(signed_transaction))

###############
# Verify signature

with open("keys/"+sender+"_pub.pem", "rb") as file:
    try:
        keys=RSA.importKey(file.read())
    except ValueError:
        print("ERROR: Failed to load RSA keys")
    file.close()

t = signed_transaction["transaction"]
s = signed_transaction['signature']
s = bytes.fromhex(s)
msg = json.dumps(t, sort_keys=True)
h = SHA256.new(msg.encode('UTF-8'))
try:
    pkcs1_15.new(keys.publickey()).verify(h,s)
    print("The signature is valid.")
except ValueError:
    print("Verification error")

