#/bin/bash

out=$(curl http://www.topology-zoo.org/maps/ )

out1=$(echo $out | grep -P "<a href=.+?>" -o)

IFS=$'\n'

cd ~/Documents/topologyzoo-picture

for i in $out1 ; do
     k=$(echo $i | cut -d \" -f 2); 
     kl=$(echo $k | cut -b 1);
    if [ $kl = '?' ]; then
        echo 'skip'; 
    elif [ $kl = '/' ];
        then echo 'skip';
    else 
        wget "http://www.topology-zoo.org/maps/$k";
        echo $k;
    fi
done



