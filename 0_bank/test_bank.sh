curl http://localhost:5000/

curl http://localhost:5000/transactions -d '{"sender":"Alice", "receiver":"Bob", "amount":10, "secret":"abcd"}' --header "Content-Type: application/json" -XPOST

curl http://localhost:5000/accounts?owner=Alice\&secret=abcd
curl http://localhost:5000/accounts?owner=Bob\&secret=dcba

curl http://localhost:5000/transactions -d '{"sender":"Bob", "receiver":"Eve", "amount":10, "secret":"dcba"}' --header "Content-Type: application/json" -XPOST

curl http://localhost:5000/accounts?owner=Bob\&secret=dcba
curl http://localhost:5000/accounts?owner=Eve\&secret=1234

