# Editing a Code Object

## Generic Code
If the code is a Generic code, just edit the row in the codes table after performing basic checks

## Element Code
If the code is an Element code
* if element id and element type is editied, cross check element info from pwc db
* edit the row in codes table after performing basic checks

## Approved Element Outage Code
If the code is an Approved Element Outage Code
* if approval_id is edited, cross check approval info from pwc db. Allow approval_id changes only when rto_id is null
* if execution time is edited and rto_id is null and is_source_deleted is False, then create a new real_time_outage entry in pwc db and link the real_time_outage id to this code row
* if execution time is edited and rto_id is not null and is_source_deleted is False, then edit the timings in real_time_outage entry in pwc db
* edit the row in codes table after performing basic checks

## Element Outage Code
If the code is an Element Outage Code
* if element id or element_type id is edited, check if they are valid. Allow element changes only when rto_id is null
* if execution time is edited and rto_id is null and is_source_deleted is False, then create a new real_time_outage entry in pwc db and link the real_time_outage id to this code row
* if execution time is edited and rto_id is not null and is_source_deleted is False, then edit the timings in real_time_outage entry in pwc db
* edit the row in codes table after performing basic checks

## Element Revival Code
If the code is an Element Revival Code
* Do not allow rto_id, element_id, element_type changes
* edit the row in codes table after performing basic checks
* If execution time is edited and rto_id is not null and is_source_deleted is False, then edit the timings in real_time_outage entry in pwc db