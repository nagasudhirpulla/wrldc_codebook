## Tracking Deleted Outages in Outage software

* After the code that is associated with an outage is issued in code book, the original outage can be deleted from the table.
* Hence we need to track deleted outages and updated the 'is_deleted_at_src' flag in the codes table
* For this purpose we create a trigger that populates the ```REPORTING_WEB_UI_UAT.DELETED_OUTAGES``` table each the rows are deleted from ```REPORTING_WEB_UI_UAT.REAL_TIME_OUTAGE``` table.
* The code_book app will run a job each 5 mins to see if new deleted outages are populated in the ```REPORTING_WEB_UI_UAT.DELETED_OUTAGES``` table. The last processed deleted outage will be tracked by the app by maintaining an application state in db like "last_processed_deleted_outage_timestamp"
* If new deleted outages are found the ```is_deleted_at_src``` flag for the corresponding codes will be set
