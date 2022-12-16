#!/bin/bash

echo Transaction from 5301 to 5302 amount 100
curl http://localhost:5301/sender -d '{"receiver": "5302", "amount": 100}' --header "Content-Type: application/json" -XPOST

echo Transaction from 5301 to 5300 amount 100
curl http://localhost:5301/sender -d '{"receiver": "5300", "amount": 100}' --header "Content-Type: application/json" -XPOST

echo Transaction from 5300 to 5301 amount 100
curl http://localhost:5300/sender -d '{"receiver": "5301", "amount": 100}' --header "Content-Type: application/json" -XPOST

echo Transaction from 5301 to 5300 amount 100
curl http://localhost:5301/sender -d '{"receiver": "5300", "amount": 100}' --header "Content-Type: application/json" -XPOST

echo Accounts on 5300
curl http://localhost:5300/accounts 

echo Accounts on 5301 
curl http://localhost:5301/accounts 

echo Accounts on 5302
curl http://localhost:5302/accounts 

echo Transaction from 5302 to 5300 amount 150
curl http://localhost:5302/sender -d '{"receiver": "5300", "amount": 150}' --header "Content-Type: application/json" -XPOST

