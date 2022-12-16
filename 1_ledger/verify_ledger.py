#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 22:29:27 2022

@author: sawickib
"""

import requests
import json
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

r = requests.get('http://localhost:5000/transactions')
ledger = r.json()

for i in range(len(ledger)):
    if i==0 and ledger[i]['transaction']['sender']=='GENESIS':
        print("GENESIS OK")
        continue
    txt=json.dumps(ledger[i-1], sort_keys=True)
    h = SHA256.new(txt.encode('utf-8'))
    if ledger[i]['prev_hash'] == h.hexdigest():
        print("Block "+str(i)+": prev_hash OK")
    else:
        print("Block "+str(i)+": prev_hash ERROR")
    
    t = ledger[i]["transaction"]
    s = ledger[i]['signature']
    sender = t['sender']
    receiver = t['receiver']
    amount = t['amount']
    s = bytes.fromhex(s)

    with open(sender+"_pub.pem", "rb") as file:
        try:
            keys=RSA.importKey(file.read())
        except ValueError:
            print("ERROR: Failed to load RSA keys")
        file.close()

    msg = json.dumps(t, sort_keys=True)
    h = SHA256.new(msg.encode('UTF-8'))
    try:
        pkcs1_15.new(keys.publickey()).verify(h,s)
        print("The signature is valid.")
        valid = True
    except ValueError:
        print("Verification error")
        valid = False
    
