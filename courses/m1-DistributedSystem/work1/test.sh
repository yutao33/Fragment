#!/bin/bash

NUM=1000

function test {
	echo $1;
	(./DictClient 127.0.0.1 4500 methodology > $1.txt )&
}

for ((i=1;i<=$NUM;i++)) ; do
	test $i ;
done

wait

for ((i=1;i<=$NUM;i++)) ; do
	cat $i.txt;
	rm $i.txt;
done



