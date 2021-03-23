#!/bin/bash

while IFS='$\n' read -r -t 10 line
do
python3 Search.py $line
done
exit 0
