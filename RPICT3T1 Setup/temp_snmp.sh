#!/bin/bash
#!/usr/bin/python

if [ "$1" = "-g" ]
 
then

echo .1.3.6.1.2.1.25.1.7.1

echo integer #set the OID as INTEGER

templine=$(tail -n 1 /usr/local/bin/Logging_Data/temperature.log)



currentsensor1=$(echo $templine | cut -d 'C' -f -3)
currentvalue1=$(echo $currentsensor1 | cut -d ' ' -f 6-) 
tempvalue1=$(echo $currentvalue1 | cut -d ' ' -f -1)

echo $tempvalue1





fi

exit 0
