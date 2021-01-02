# Real Time Outage Manipulation

## Create Real time Outage
* create reason id if required and get the required reason id for creation of outage
* create row in pwc real time outage table after performing all checks

## Edit Real time outage
* do not allow to edit element id and element type
* if reason is edited, create reason id if required and get the required reason id for editing of outage
* edit the outage row in pwc db after performing all checks
* if real_time_outage id is associated with any row in code table, then edit code table row also

## Delete Real time outage
* give this privilege to only admin level users
* delete the row in real time outage table
* if real_time_outage id is associated with any row in code table, then set is_deleted_at_src column to true in that row