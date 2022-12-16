from flask import Flask, request
import json

app = Flask(__name__)

Accounts = {}
Accounts['Alice'] = {'secret':'abcd', 'balance':100}
Accounts['Bob'] = {'secret':'dcba', 'balance':100}
Accounts['Eve'] = {'secret':'1234', 'balance':100}

Transactions = []

@app.post('/transactions')
def post_transactions():
    t = request.json
    sender = t['sender']
    receiver = t['receiver']
    amount = t['amount']
    secret = t['secret']
    msg = "Transaction rejected"
    if sender in Accounts and secret==Accounts[sender]['secret']:
        if receiver in Accounts:
            msg = "Accepted transaction: "+str(amount)+" from "+sender+" to "+receiver
            Transactions.append(t)
            Accounts[sender]['balance'] += -amount
            Accounts[receiver]['balance'] += amount
    return msg+"\n", 201


@app.get('/accounts')
def get_nodes():
    owner = request.args.get('owner')
    secret = request.args.get('secret')
    if owner:
        if Accounts[owner]['secret'] == secret:
            msg = owner+" balance: "+str(Accounts[owner]['balance'])
    else:
        msg = "Authentication error"
    return msg+"\n"

@app.route('/')
def index():
    return "Welcome to Confidential Bank\n"

if __name__ == '__main__':
    app.run(debug=True)
    
