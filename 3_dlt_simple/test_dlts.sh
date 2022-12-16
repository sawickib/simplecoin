curl http://localhost:5300/

echo Transaction from 5301 to 5302 amount 10
curl http://localhost:5301/sender -d '{"receiver": "5302", "amount": 10}' --header "Content-Type: application/json" -XPOST

echo Transaction from 5301 to 5302 amount 10
curl http://localhost:5301/sender -d '{"receiver": "5302", "amount": 10}' --header "Content-Type: application/json" -XPOST

echo Transaction from 5301 to 5302 amount 10
curl http://localhost:5301/sender -d '{"receiver": "5302", "amount": 10}' --header "Content-Type: application/json" -XPOST

echo Transaction from 5301 to 5302 amount 10
curl http://localhost:5301/sender -d '{"receiver": "5302", "amount": 10}' --header "Content-Type: application/json" -XPOST

echo Transaction from 5301 to 5302 amount 10
curl http://localhost:5301/sender -d '{"receiver": "5302", "amount": 10}' --header "Content-Type: application/json" -XPOST

echo Accounts on 5300
curl http://localhost:5300/accounts 

echo Accounts on 5301 
curl http://localhost:5301/accounts 

echo Accounts on 5302
curl http://localhost:5302/accounts 

echo Accounts on 5303
curl http://localhost:5303/accounts 

echo Accounts on 5304
curl http://localhost:5304/accounts 
