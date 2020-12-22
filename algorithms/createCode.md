# Creating a Code Object

## Generic Code
If the code is a Generic code, create a row in the codes table after performing basic checks

## Element Code
If the code is an Element code
* cross check element info from pwc db
* create a row in the codes table after performing basic checks

## Approved Element Outage Code
If the code is an Approved Element Outage Code
* cross check shutdown request id from pwc db
* create a code row after performing all basic checks
* if execution time is mentioned in the code info, then create a row in pwc real_time_outage table and link that created pwc id to the code object (edit code execution time operation)

## Element Outage Code
If the code is an Element Outage Code
* cross check element info from pwc db
* create a code row after performing all basic checks
* if execution time is mentioned in the code info, then create a row in pwc real_time_outage table and link that created pwc id to the code object (edit code execution time operation)

## Element Revival Code
If the code is an Element Revival Code
* cross check real_time_outage id from pwc db and ensure that the revival time is null
* create a code row after performing all basic checks
* if execution time is mentioned in the code info, then edit the revial time info and revival remarks for the outage row in pwc real_time_outage table (edit code execution time operation)