#!/bin/bash

# WARNING: This script will REMOVE existing portfolio*.csv files
# without prompting.

myfile="$1"

if [ "$myfile" = "" ] ; then
	echo " "
	echo "USAGE: $0 [basket.txt]"
	echo " "
	exit 0
fi

rm -f portfolio*csv
python3 basket-simulator.py $myfile
echo "Analysis for $myfile";
echo " ";
python3 analyse-results.py
echo "...end of analysis for $myfile";
rm -f portfolio*csv
