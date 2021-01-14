# Creating a Code Object

## Generic Code
* If the code is a Generic code, create a row in the codes table after performing basic checks
* code_type will be considered as "Generic"
* code_issue_time will be considered as present time
* code_issued_by will be considered as current logged in user
* uniqueness of code is currently not being checked
* code field not null validation will be performed
* other RLDC codes, if present, will be derived by comma separation
* code description not null validation will be performed

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
* if execution time is mentioned in the code info, then edit the revival time info and revival remarks for the outage row in pwc real_time_outage table (edit code execution time operation)

## Note
* While creating a new row in real time outages table use Coalesce(Max(ID),0) + 1 and return it into a varible for consumption by our python code - https://cx-oracle.readthedocs.io/en/latest/user_guide/txn_management.html#autocommitting, 
https://stackoverflow.com/a/17211129/2746323