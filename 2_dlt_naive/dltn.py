#!/usr/bin/env python3

from flask import Flask, request
import json
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from datetime import datetime
import sys
import requests

app = Flask(__name__)

Nodes = {}
Transactions = []
Accounts = {}

@app.route('/')
def index():
    return "Welcome to Naive Distributed Ledger\n"

@app.post('/sender')
def post_sender():
    transaction = request.json
    transaction['sender'] = my_name
    sender = my_name
    receiver = transaction['receiver']
    amount = transaction['amount']
    msg = "Transaction OK"
    code = 201
    if(cheater_mode):
       print("CHEATER MODE")
    if Accounts[sender] >= amount or cheater_mode:
        txt = json.dumps(transaction, sort_keys=True)
        h = SHA256.new(txt.encode('utf-8'))
        s = pkcs1_15.new(my_keys).sign(h)
        signature = s.hex()
        st = add_transaction(sender, receiver, amount, signature)
        for name in Nodes:
            send = False
            if name != my_name:
                if not cheater_mode:
                    send = True
                else:
                    if name == receiver:
                        send = True
            if send:
                r = requests.post(Nodes[name]['url']+'/transactions', json=st)
                code = r.status_code
                if code != 201:
                    msg = "Error: transaction rejected by "+name
    else:
        msg = "Insufficient funds"
        code = 409

    recalculate_accounts()
#    print(msg)
    return msg+"\n", code

@app.post('/transactions')
def post_transactions():
    signed_transaction = request.json
    t = signed_transaction["transaction"]
    sender = t['sender']
    receiver = t['receiver']
    amount = t['amount']
    valid = check_signature(signed_transaction)
    if valid and Accounts[sender] >= amount:
        Transactions.append(signed_transaction)
        msg = "Transaction accepted"
        recalculate_accounts()       
        code = 201
    else:
        msg = "Transaction rejected"
        code = 409
    return msg+"\n", code


@app.get('/transactions')
def get_transactions():
    return Transactions      

@app.get('/accounts')
def get_accounts():
    return Accounts

@app.post('/nodes')
def post_nodes():
    new_node = request.json
    name = new_node['name']
    if name not in Nodes:
        Nodes[name] = {}
        Nodes[name]['name'] = name
        Nodes[name]['url'] = new_node['url']
        Nodes[name]['pubkey'] = new_node['pubkey']
    return "\n", 201

@app.get('/nodes')
def get_nodes():
    return Nodes
    
def recalculate_accounts():
    for ts in Transactions:
        sender = ts['transaction']['sender'] 
        receiver = ts['transaction']['receiver']
        amount = ts['transaction']['amount']
        if sender == 'GENESIS':
            continue
        if sender == 'DEPOSIT':
            Accounts[receiver] = amount
            continue
            
        if check_signature(ts):
            Accounts[sender] += -amount
            Accounts[receiver] += amount


def add_transaction(sender, receiver, amount, signature=''):
    transaction = {'transaction':{'amount':amount, 'receiver':receiver, 'sender':sender}}
    transaction['signature'] = signature
    txt = json.dumps(Transactions[-1], sort_keys=True)
    h = SHA256.new(txt.encode('utf-8'))
    transaction['prev_hash'] = h.hexdigest()
    transaction['datetime'] = str(datetime.now())
    Transactions.append(transaction)
    return transaction

def check_signature(transaction):
    valid = False
    sender = transaction['transaction']['sender']
    keys=RSA.importKey(Nodes[sender]['pubkey'])
    t = transaction['transaction']
    s = transaction['signature']
    s = bytes.fromhex(s)
    msg = json.dumps(t, sort_keys=True)
    h = SHA256.new(msg.encode('UTF-8'))
    try:
        pkcs1_15.new(keys.publickey()).verify(h,s)
        valid = True
    except ValueError:
        print("Verification error")
    return valid

def connect(url):
    r = requests.get(url+'/nodes')
    nodes = r.json()
    for name in nodes.keys():
        if name != my_name:
           Nodes[name] = {}
           Nodes[name]['name'] = name
           Nodes[name]['url'] = nodes[name]['url']
           Nodes[name]['pubkey'] = nodes[name]['pubkey']
           requests.post(nodes[name]['url']+'/nodes', json=Nodes[my_name])

def fetch_transactions(url):
    r = requests.get(url+'/transactions')
    return r.json()

if __name__ == '__main__':
    my_name = sys.argv[1]
    my_port = my_name
    connect_url = sys.argv[2]
    cheater_mode = False
    if len(sys.argv) > 3:
        cheater_mode = True
    
    with open("keys/"+my_name+"_priv.pem", "rb") as file:
        try:
            my_keys=RSA.importKey(file.read(), passphrase='abc')
        except ValueError:
            print("ERROR: Failed to load RSA keys")
    
    Nodes[my_name] = {}
    Nodes[my_name]['name'] = my_name
    Nodes[my_name]['url'] = "http://localhost:"+my_port
    Nodes[my_name]['pubkey'] = str(my_keys.publickey().exportKey(), encoding='utf-8')  
    
    if connect_url != 'init' :
        connect(connect_url)
        Transactions = fetch_transactions(connect_url)
    else:
        Transactions.append({'transaction':{'amount':0, 'receiver':'GENESIS', 'sender':'GENESIS'}})
        add_transaction('DEPOSIT', '5300', 100)
        add_transaction('DEPOSIT', '5301', 100)
        add_transaction('DEPOSIT', '5302', 100)
        
    recalculate_accounts()
    
    print("Starting node "+my_name+" on port "+my_port)
    app.run(debug=False, port=my_port)
    
