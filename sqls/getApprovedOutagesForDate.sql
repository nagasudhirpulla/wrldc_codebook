SELECT
	SD.ID,
	SD.SHUTDOWN_REQUEST_ID,
	sr.ENTITY_ID,
	sr.ELEMENT_ID,
	sr.REASON_ID,
	sr.shutdownType,
	sr.occ_name,
	sr.elementType,
	sr.ELEMENT_NAME,
	sr.requester_name,
CASE
		WHEN SR.IS_CONTINUOUS = 1 THEN 'Continuous'
		WHEN sr.IS_CONTINUOUS = 0 THEN 'Daily'
		ELSE NULL
	END DailyCont,
	sr.REASON,
	SD.APPROVED_START_DATE,
	SD.APPROVED_END_DATE,
	sr.REQUESTER_REMARKS,
CASE
		WHEN sr.is_availed = 1 THEN 'Yes'
		WHEN sr.is_availed = 2 THEN 'NO'
		ELSE NULL
	END AvailingStatus,
	ss.STATUS,
	SD.RLDC_REMARKS,
	sr.rpc_remarks,
	sr.NLDC_REMARKS,
	sr.nldc_approval_status
FROM
	REPORTING_WEB_UI_UAT.SHUTDOWN sd
LEFT JOIN REPORTING_WEB_UI_UAT.SHUTDOWN_STATUS ss ON
	ss.ID = sd.STATUS_ID
LEFT JOIN (
	SELECT
		req.*, sot.NAME AS shutdownType, em.ENTITY_NAME AS elementType, or2.REASON, om.OCC_NAME, ud.USER_NAME AS requester_name, ss2.STATUS AS nldc_approval_status
	FROM
		REPORTING_WEB_UI_UAT.SHUTDOWN_REQUEST req
	LEFT JOIN REPORTING_WEB_UI_UAT.SHUTDOWN_OUTAGE_TYPE sot ON
		sot.ID = req.SHUT_DOWN_TYPE_ID
	LEFT JOIN REPORTING_WEB_UI_UAT.ENTITY_MASTER em ON
		em.ID = req.ENTITY_ID
	LEFT JOIN REPORTING_WEB_UI_UAT.OUTAGE_REASON or2 ON
		or2.ID = req.REASON_ID
	LEFT JOIN REPORTING_WEB_UI_UAT.OCC_MASTER om ON
		om.OCC_ID = req.OCC_ID
	LEFT JOIN REPORTING_WEB_UI_UAT.USER_DETAILS ud ON
		req.INTENDED_BY = ud.USERID
	LEFT JOIN REPORTING_WEB_UI_UAT.SHUTDOWN_STATUS ss2 ON
		req.NLDC_STATUS_ID = ss2.ID ) sr ON
	sr.ID = sd.SHUTDOWN_REQUEST_ID
WHERE
	(to_date('2020-12-22', 'YYYY-MM-DD') BETWEEN TRUNC(sd.APPROVED_START_DATE) AND TRUNC(sd.APPROVED_END_DATE))
	AND ss.STATUS = 'Approved'

/*
TODO find rpc approval status column
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