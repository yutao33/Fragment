#!/bin/bash
echo $1
for i in $(seq 1 $1); do
    echo $i
    time curl http://10.0.0.9/200M.dat > /dev/null
    sleep 1
done
