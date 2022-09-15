#!/bin/bash

elfDir=../elf/
ghidraDir=../ghidraprj/
ghidraMainDir=$1

if [ $# != 1 ]; then
    echo 引数エラー: Ghidraディレクトリの場所を入力してください。例）/Users/test/ghidra_10.1.5_PUBLIC/
    exit 1
fi

find ${elfDir} -type f -print0 | while read -d $'\0' elflist
do
	prjName=$(basename ${elflist} .bin.list)
	echo ${prjName}
	echo ${ghidraDir}${prjName}'.rep'
	if [[ -f ${ghidraDir}${prjName}'.rep' ]]; then
		echo 'hell'
	else
		while read -r elfline;
		do
			elfPath=$( echo ${elfline}| sed "s/\/mnt\/raw_firmwares/../g")
			${ghidraMainDir}support/analyzeHeadless ${ghidraDir} ${prjName} -import ${elfPath} 
		done < ${elflist}
		
	fi
done
