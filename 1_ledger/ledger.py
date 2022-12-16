#!/usr/bin/env python3

from flask import Flask, request
import json
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from datetime import datetime
app = Flask(__name__)

Accounts = {}
Accounts['16b5'] = {'balance':1000}
Accounts['1bd2'] = {'balance':1000}
Accounts['3e43'] = {'balance':1000}

Transactions = []
Transactions.append({'transaction':{'amount':0, 'receiver':'GENESIS', 'sender':'GENESIS'}})

@app.post('/transactions')
def post_transactions():
    signed_transaction = request.json
    t = signed_transaction["transaction"]
    s = signed_transaction['signature']
    sender = t['sender']
    receiver = t['receiver']
    amount = t['amount']
    s = bytes.fromhex(s)

    with open("keys/"+sender+"_pub.pem", "rb") as file:
        try:
            keys=RSA.importKey(file.read())
        except ValueError:
            print("ERROR: Failed to load RSA public key")
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
    
    msg = "Transaction rejected"
    if sender in Accounts and valid:
        if receiver in Accounts:
            msg = "Accepted transaction: "
            msg += "sender "+str(sender)+", receiver "+str(receiver)+", amount "+str(amount)
            txt=json.dumps(Transactions[-1], sort_keys=True)
            h = SHA256.new(txt.encode('utf-8'))
            signed_transaction['prev_hash'] = h.hexdigest()
            signed_transaction['datetime'] = str(datetime.now())
            Transactions.append(signed_transaction)
            Accounts[sender]['balance'] += -amount
            Accounts[receiver]['balance'] += amount
    return msg+"\n", 201

@app.get('/transactions')
def get_transactions():
    return Transactions

@app.get('/accounts')
def get_accounts():
    for a in Accounts.keys():
        with open("keys/"+a+"_pub.pem", "rb") as file:
            try:
                pubkey=file.read()
            except ValueError:
                print("ERROR: Failed to load RSA public key")
            file.close()
        Accounts[a]['pubkey']=str(pubkey)
    return Accounts
    
@app.route('/')
def index():
    return "Welcome to Central Open Ledger Bank\n"

if __name__ == '__main__':
    app.run(debug=True)
    
