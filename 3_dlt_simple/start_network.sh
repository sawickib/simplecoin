#!/bin/bash

echo Starting node 5300
python3 dlts.py 5300 init &> log0 &
sleep 1

echo Starting node 5301
python3 dlts.py 5301 http://localhost:5300 &> log1 &
sleep 1

echo Starting node 5302
python3 dlts.py 5302 http://localhost:5300 &> log2 &
sleep 1

echo Starting node 5303
python3 dlts.py 5303 http://localhost:5300 &> log3 &
sleep 1

echo Starting node 5304
python3 dlts.py 5304 http://localhost:5300 &> log4 &
sleep 1

