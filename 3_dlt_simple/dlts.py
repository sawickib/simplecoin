#!/usr/bin/env python3

from flask import Flask, request
import json
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from datetime import datetime
import sys
import requests
import random

app = Flask(__name__)

Nodes = {}
Blocks = []
Accounts = {}

# Confirmation rejection coefficient
alpha = 0.5
# Required confimation ratio
beta = 0.5

@app.route('/')
def index():
    return "===\n= Welcome to Simple Voting Distributed Ledger\n===\n"

@app.post('/confirm')
def post_confirm():
    block = request.json
    t = block["transaction"]
    sender = t['sender']
    amount = t['amount']
    valid = check_signature(block)
    if valid and Accounts[sender] >= amount and random.random()>alpha:
        signature = sign_transaction(t)
        if 'confirmations' not in block:
           block['confirmations']={}
        block['confirmations'][my_name] = signature
        msg = block
        code = 200
    else:
        msg = "Error: refusal to confirm" 
        code = 409
    return block, code


@app.post('/sender')
def post_sender():
    transaction = request.json
    transaction['sender'] = my_name
    sender = my_name
    receiver = transaction['receiver']
    amount = transaction['amount']
    msg = ""
    code = 201
    if Accounts[sender] >= amount:
        signature = sign_transaction(transaction)
        block = create_block(sender, receiver, amount, signature)
        
        # Ask for confirmations
        for name in Nodes:
            if name != my_name:
                r = requests.post(Nodes[name]['url']+'/confirm', json=block)
                code = r.status_code
                if code == 200:
                    block = r.json()
                else:
                    msg += "   Error: confirmation denied by "+name+"\n"

        number_of_confirmations = check_confirmations(block)
        msg = "   confirmed by "+str(number_of_confirmations)+" nodes\n"

        # Propagate new block
        for name in Nodes:
            r = requests.post(Nodes[name]['url']+'/blocks', json=block)
            code = r.status_code
            if code != 201:
                msg += "   Error: transaction rejected by "+name+"\n"
    else:
        msg += "  Insufficient funds\n"
        code = 409


    calculate_accounts()
    return msg, code

@app.post('/blocks')
def post_blocks():
    block = request.json
    t = block["transaction"]
    sender = t['sender']
    receiver = t['receiver']
    amount = t['amount']
    number_of_confirmations = check_confirmations(block)
    if number_of_confirmations+1 > len(Nodes.keys())*beta:
        Blocks.append(block)
        msg = "Block accepted"
        calculate_accounts()       
        code = 201
    else:
        msg = "Block rejected"
        code = 409
    return msg+"\n", code


@app.get('/blocks')
def get_blocks():
    return Blocks      

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
    
def calculate_accounts():
    for block in Blocks:
        sender = block['transaction']['sender'] 
        receiver = block['transaction']['receiver']
        amount = block['transaction']['amount']
        if sender == 'GENESIS':
            continue
        if sender == 'DEPOSIT':
            Accounts[receiver] = amount
            continue
            
        if check_signature(block):
            Accounts[sender] += -amount
            Accounts[receiver] += amount


def create_block(sender, receiver, amount, signature=''):
    block = {'transaction':{'amount':amount, 'receiver':receiver, 'sender':sender}}
    block['signature'] = signature
    txt = json.dumps(Blocks[-1], sort_keys=True)
    h = SHA256.new(txt.encode('utf-8'))
    block['prev_hash'] = h.hexdigest()
    block['datetime'] = str(datetime.now())
    return block

def sign_transaction(transaction):
    txt = json.dumps(transaction, sort_keys=True)
    h = SHA256.new(txt.encode('utf-8'))
    s = pkcs1_15.new(my_keys).sign(h)
    signature = s.hex()
    return signature
    
def check_signature(block):
    valid = False
    sender = block['transaction']['sender']
    keys=RSA.importKey(Nodes[sender]['pubkey'])
    t = block['transaction']
    s = block['signature']
    s = bytes.fromhex(s)
    msg = json.dumps(t, sort_keys=True)
    h = SHA256.new(msg.encode('UTF-8'))
    try:
        pkcs1_15.new(keys.publickey()).verify(h,s)
        valid = True
    except ValueError:
        print("  Verification error")
    return valid

def check_confirmations(block):
    sender = block['transaction']['sender']
    t = block['transaction']
    msg = json.dumps(t, sort_keys=True)
    h = SHA256.new(msg.encode('UTF-8'))
    
    no_confirm = 0
    for name in block['confirmations'].keys():
        keys=RSA.importKey(Nodes[name]['pubkey'])
        s = block['confirmations'][name]
        s = bytes.fromhex(s)
        try:
            pkcs1_15.new(keys.publickey()).verify(h,s)
            no_confirm += 1
        except ValueError:
            print("  Verification error")

    return no_confirm


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

def fetch_blocks(url):
    r = requests.get(url+'/blocks')
    return r.json()

def my_node():
    node = {}
    node['name'] = my_name
    node['url'] = "http://localhost:"+my_port
    node['pubkey'] = str(my_keys.publickey().exportKey(), encoding='utf-8')
    return node
    
def init_blocks():
    Blocks.append({'transaction':{'amount':0, 'receiver':'GENESIS', 'sender':'GENESIS'}})
    Blocks.append(create_block('DEPOSIT', '5300', 100))
    Blocks.append(create_block('DEPOSIT', '5301', 100))
    Blocks.append(create_block('DEPOSIT', '5302', 100))
    Blocks.append(create_block('DEPOSIT', '5303', 100))
    Blocks.append(create_block('DEPOSIT', '5304', 100))

def load_my_keys():
    with open("keys/"+my_name+"_priv.pem", "rb") as file:
        try:
            my_keys=RSA.importKey(file.read(), passphrase='abc')
        except ValueError:
            print("  ERROR: Failed to load RSA keys")
    return my_keys

if __name__ == '__main__':
    my_name = sys.argv[1]
    my_port = my_name
    connect_url = sys.argv[2]
    
    my_keys = load_my_keys()
    Nodes[my_name] = my_node()
    
    if connect_url != 'init' :
        connect(connect_url)
        Blocks = fetch_blocks(connect_url)
    else:
        init_blocks()
        
    calculate_accounts()
    
    print("  Starting node "+my_name+" on port "+my_port)
    app.run(debug=False, port=my_port)
    
