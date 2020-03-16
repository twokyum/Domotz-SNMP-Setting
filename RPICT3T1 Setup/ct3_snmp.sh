#!/bin/bash
#!/usr/bin/python

if [ "$1" = "-g" ]
 
then

echo .1.3.6.1.2.1.25.1.7.4

echo integer #set the OID as INTEGER

templine=$(tail -n 1 /usr/local/bin/Logging_Data/temperature.log)



currentsensor3=$(echo $templine | cut -d 'C' -f -5)
currentvalue3=$(echo $currentsensor3 | cut -d ' ' -f 13-) 

echo $currentvalue3



fi

exit 0
