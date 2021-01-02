# Types of Code
* Generic Code
* Approved Outage Code
* Element Outage Code
* Element Revival Code
* Element Code

## Attributes of a Generic Code
* id - auto increment db serial int
* Code type - Generic/ApprovedOutage/Outage/Revival/Element
* Code issue time - datetime
* Code - user defined string
* Other LDC Codes - array of strings
* Code description - string
* Code execution time - datetime
* Code Tags - string (like FTC, Violation message etc. Tags master table will be present)
* Code issued by - person id
* Is code cancelled - yes/no (boolean)

## Extra attributes for code issued for an approved outage - Approved Outage Code
* sd_req_id - integer from pwc_db (id w.r.t. pwc shutdown_request table)
* rto_id - integer from pwc_db (id w.r.t pwc real time outages table)
* is_deleted_at_src - boolean (true if the outage entry is deleted in pwc db)
### cached columns for analytics and display
* pwc_element_id - integer from pwc db (id w.r.t pwc element table)
* pwc_element_type_id  - integer from pwc_db (id w.r.t pwc entity_master)
* outage_type_id - integer from pwc_db (id w.r.t to pwc shutdown_outage_type table)
* element_name - string from pwc_db
* pwc_element_type - string from pwc_db (string w.r.t pwc entity_master)
* outage_type - string from pwc_db (w.r.t to pwc shutdown_outage_type table)

## Extra attributes for code issued for an element outage - Element Outage Code
* rto_id - integer from pwc_db (id w.r.t pwc real time outages table)
* is_deleted_at_src - boolean (true if the outage entry is deleted in pwc db)
### cached columns for analytics and display
* pwc_element_id - integer from pwc db (id w.r.t pwc element table)
* pwc_element_type_id  - integer from pwc_db (id w.r.t pwc entity_master)
* outage_type_id - integer from pwc_db (id w.r.t to pwc shutdown_outage_type table)
* element_name - string from pwc_db
* pwc_element_type - string from pwc_db (string w.r.t pwc entity_master)
* outage_type - string from pwc_db (w.r.t to pwc shutdown_outage_type table)

## Extra attributes for code issued for an element revival - Element Revival Code
* rto_id - integer from pwc_db (id w.r.t pwc real time outages table)
* is_deleted_at_src - boolean (true if the outage entry is deleted in pwc db)
### cached data for analytics and display
* pwc_element_id - integer from pwc db (id w.r.t pwc element table)
* pwc_element_type_id  - integer from pwc_db (id w.r.t pwc entity_master)
* element_name - string from pwc_db
* pwc_element_type - string from pwc_db (string w.r.t pwc entity_master)

## Extra attributes for code issued for an element - Element Code
* pwc_element_id - integer from pwc db (id w.r.t pwc element table)
* pwc_element_type_id  - integer from pwc_db (id w.r.t pwc entity_master)
* element_name - string from pwc_db
* pwc_element_type - string from pwc_db (string w.r.t pwc entity_master)


# Columns of Outage Code Table
* id - auto increment db serial int
* Code type - Generic/ApprovedOutage/Outage/Revival/Element
* Code issue time - datetime
* Code - user defined string
* Other LDC Codes - array of strings
* Code description - string
* Code execution time - datetime
* Code Tags - string (like FTC, Violation message etc. Tags master table will be present)
* Code issued by - person id
* Is code cancelled - yes/no (boolean)
* sd_req_id - integer from pwc_db (id w.r.t. pwc shutdown_request table)
* rto_id - integer from pwc_db (id w.r.t pwc real time outages table)
* is_deleted_at_src - boolean (true if the outage entry is deleted in pwc db)
* pwc_element_id - integer from pwc db (id w.r.t pwc element table)
* pwc_element_type_id  - integer from pwc_db (id w.r.t pwc entity_master)
* outage_type_id - integer from pwc_db (id w.r.t to pwc shutdown_outage_type table)
* element_name - string from pwc_db
* pwc_element_type - string from pwc_db (string w.r.t pwc entity_master)
* outage_type - string from pwc_db (w.r.t to pwc shutdown_outage_type table)
* is_deleted - this field will be true if the code object is deleted