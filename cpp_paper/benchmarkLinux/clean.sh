#!/bin/bash


cd testingData

for dir in $(ls)
do

    if [ $dir == '.svn.' ]
    then
        continue
    fi

    if [ ! $dir == '_DATA_' ]
    then
        cd $dir

        rm -R statistic
        mkdir statistic

        cd approxData
        for sdir in $(ls)
        do
            rm -R $sdir
            mkdir $sdir
        done
        cd ..

        cd compressedData
        for sdir in $(ls)
        do
            rm -R $sdir
            mkdir $sdir
        done
        cd ..

        cd ..
    fi
done

cd ..
