curl http://localhost:5000/
curl http://localhost:5000/transactions 

echo "Transaction 16b5->1bd2"
curl http://localhost:5000/transactions -d '{"transaction": {"sender": "16b5", "receiver": "1bd2", "amount": 102}, "signature": "3534167ed15cabe0f0caf36464fa6a1fac850757b240115b5a6f88bead199eaa5c3dad15d7357424fa2c0a93e236a0f26c5b1a32c128a711618ba165b1c43c2de70f1d5790c4a194d2b3ad5589e2e5c3f64e1947b5883859917897957f276c8aa79d9236d2fa48bd8c76f478df30eaddc57efc1b9f3c093888b5ac135914e3d3"}' --header "Content-Type: application/json" -XPOST

echo "Transaction 16b5->3e43"
curl http://localhost:5000/transactions -d '{"transaction": {"sender": "16b5", "receiver": "3e43", "amount": 102}, "signature": "896962fb8dfb653aac8a9f5d887cdd6188b5179aafa7e91739933406d1d0ee0299f97839a487ef988d3adea87c1cc40d07c744a1f65fb5c8d7bba9ce845af48e4f1fac99a28aebd59628907f93fa1663769054dd3a0181dfdb298e25f038dbafe33d6b7188f94734cfa0fe2c42e8866c300bfea83d9a09c04a3157d341110f91"}' --header "Content-Type: application/json" -XPOST

curl http://localhost:5000/transactions 


