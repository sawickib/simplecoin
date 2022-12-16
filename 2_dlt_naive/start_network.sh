#!/bin/bash

echo Starting node 5300
python3 dltn.py 5300 init &> log0 &
sleep 1

echo Starting node 5301
python3 dltn.py 5301 http://localhost:5300 &> log1 &
#python3 dltn.py 5301 http://localhost:5300 cheater &> log1 &
sleep 1

echo Starting node 5302
python3 dltn.py 5302 http://localhost:5300 &> log2 &
sleep 1


