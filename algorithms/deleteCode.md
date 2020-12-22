# Deleting a Code Object

## Generic Code
If the code is a Generic code, just delete the row in the codes table

## Element Code
If the code is an Element code, just delete the row in the codes table

## Approved Element Outage Code
Give the approved outage code delete previlage only to admin role users
If the code is an Approved Element Outage Code
* do not allow delete, if the code has a corresponding revival code
* if the code has an rto_id associated with it, then delete the entry from pwc real_time_outage table
* delete the row from codes table

## Element Outage Code
Give the element outage code delete previlage only to admin role users
If the code is an Element Outage Code
* do not allow delete, if the code has a corresponding revival code
* if the code has an rto_id associated with it, then delete the entry from pwc real_time_outage table
* delete the row from codes table

## Element Revival Code
Give the element revival code delete previlage only to admin role users
If the code is an Element Revival Code
* if the code has an rto_id associated with it, then delete the entry from pwc real_time_outage table
* delete the row from codes table