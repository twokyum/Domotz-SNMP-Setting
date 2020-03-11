
#!/bin/bash
#!/usr/bin/python

if [ "$1" = "-g" ]
 
then



echo .1.3.6.1.2.1.25.1.7.1

echo integer #set the OID as INTEGER

templine=$(tail -n 1 /usr/local/bin/Logging_Data/temperature.log)

tempvalue=$(echo $templine | cut -d ' ' -f 6-)

echo $tempvalue 


fi

exit 0
