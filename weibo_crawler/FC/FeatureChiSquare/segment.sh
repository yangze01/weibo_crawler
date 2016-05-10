#!/bin/bash



path=$1
path1=$2
for file in `ls  $path`
do
	f=$path$file
        rf=$path1$file
	crf_test -m model_file $f > $rf
done
