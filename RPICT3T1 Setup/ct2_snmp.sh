#!/bin/bash
#!/usr/bin/python

if [ "$1" = "-g" ]
 
then

echo .1.3.6.1.2.1.25.1.7.3

echo integer #set the OID as INTEGER

templine=$(tail -n 1 /usr/local/bin/Logging_Data/temperature.log)




currentsensor2=$(echo $templine | cut -d 'C' -f -4)
currentvalue2=$(echo $currentsensor2 | cut -d ' ' -f 11-) 


echo $currentvalue2




fi

exit 0
