SELECT
	rto.ID AS pwc_id,
	rto.ELEMENT_ID,
	rto.ELEMENTNAME AS ELEMENT_NAME,
	rto.ENTITY_ID,
	ent_master.ENTITY_NAME,
	gen_unit.installed_capacity AS CAPACITY,
	rto.OUTAGE_DATE AS OUTAGE_DATETIME,
	rto.REVIVED_DATE AS REVIVED_DATETIME,
	rto.CREATED_DATE AS CREATED_DATETIME,
	rto.MODIFIED_DATE AS MODIFIED_DATETIME,
	sd_tag.name AS shutdown_tag,
	rto.SHUTDOWN_TAG_ID,
	sd_type.name AS shutdown_typename,
	rto.SHUT_DOWN_TYPE AS SHUT_DOWN_TYPE_ID,
	rto.OUTAGE_REMARKS,
	reas.reason,
	rto.REASON_ID,
	rto.REVIVAL_REMARKS,
	rto.REGION_ID,
	rto.SHUTDOWNREQUEST_ID,
	rto.OUTAGE_TIME,
	rto.REVIVED_TIME
FROM
	REPORTING_WEB_UI_UAT.real_time_outage rto
LEFT JOIN REPORTING_WEB_UI_UAT.outage_reason reas ON
	reas.id = rto.reason_id
LEFT JOIN REPORTING_WEB_UI_UAT.shutdown_outage_tag sd_tag ON
	sd_tag.id = rto.shutdown_tag_id
LEFT JOIN REPORTING_WEB_UI_UAT.shutdown_outage_type sd_type ON
	sd_type.id = rto.shut_down_type
LEFT JOIN REPORTING_WEB_UI_UAT.entity_master ent_master ON
	ent_master.id = rto.ENTITY_ID
LEFT JOIN REPORTING_WEB_UI_UAT.generating_unit gen_unit ON
	gen_unit.id = rto.element_id
WHERE
	(TRUNC(rto.OUTAGE_DATE) BETWEEN to_date('2020-12-23') AND to_date('2020-12-23'))
	OR (TRUNC(rto.revived_date) BETWEEN to_date('2020-12-23') AND to_date('2020-12-23'))