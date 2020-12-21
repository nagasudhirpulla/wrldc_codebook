SELECT
	sr.*
FROM
	REPORTING_WEB_UI_UAT.SHUTDOWN_REQUEST sr
LEFT JOIN OUTAGE_TEST.SHUTDOWN_STATUS sh_status ON
	SH_STATUS.ID = sr.STATUS_ID
WHERE
	SH_STATUS.STATUS = 'Approved'
	AND (TO_DATE('2020-12-21', 'YYYY-MM-DD') BETWEEN trunc(sr.APPROVED_START_DATE) AND trunc(sr.APPROVED_END_DATE))
	AND sr.IS_AVAILED = 1
	AND sr.IS_ADMIN_APPROVED = 1
	AND (sr.occ_id IS NULL OR sr.occ_id = 25)

/*
In real time outages table,
USER_DETAILS table has user ids for createdBy and modifiedBy columns

request_type_id refers to shutdown_outage type

entity_id refers to entity_master that has info about element type

element_id has id of element in corresponding table
For example element_id refers to AC_TRANSMISSION_LINE_CIRCUIT table if element_id is 14

shutdown_type column refers to shutdown outage type table

reason_id refers to outage_reason table

shutdown_request_id refers to shutdown_request table

shutdown_outage_tag refers to shutdown_outage_tag table

region_id refers to region_master table
*/