SELECT
	rto.id,
	rto.entity_id,
	rto.element_id,
	rto.entity_name AS elementType,
	rto.SHUT_DOWN_TYPE_NAME,
	rto.elementname,
	trunc(rto.outage_date) AS outage_date,
	rto.outage_time,
	rto.reason,
	rto.shutdown_tag,
	rto.outage_remarks
FROM
	(
	SELECT
		outages.*, ent_master.ENTITY_NAME, reas.reason, sd_type.name AS SHUT_DOWN_TYPE_NAME, sd_tag.name AS shutdown_tag, to_char(outages.OUTAGE_DATE , 'YYYY-MM-DD')|| ' ' || outages.OUTAGE_TIME AS out_date_time
	FROM
		reporting_web_ui_uat.REAL_TIME_OUTAGE outages
	LEFT JOIN reporting_web_ui_uat.outage_reason reas ON
		reas.id = outages.reason_id
	LEFT JOIN reporting_web_ui_uat.entity_master ent_master ON
		ent_master.id = outages.ENTITY_ID
	LEFT JOIN reporting_web_ui_uat.shutdown_outage_tag sd_tag ON
		sd_tag.id = outages.SHUTDOWN_TAG_ID
	LEFT JOIN reporting_web_ui_uat.shutdown_outage_type sd_type ON
		sd_type.id = outages.shut_down_type ) rto
INNER JOIN (
	SELECT
		element_id, entity_id, MAX(to_char(OUTAGE_DATE , 'YYYY-MM-DD')|| ' ' || OUTAGE_TIME) AS out_date_time
	FROM
		reporting_web_ui_uat.REAL_TIME_OUTAGE
	GROUP BY
		entity_id, ELEMENT_ID) latest_out_info ON
	((latest_out_info.entity_id = rto.entity_id)
	AND (latest_out_info.element_id = rto.element_id)
	AND (latest_out_info.out_date_time = rto.out_date_time))
WHERE rto.REVIVED_TIME IS NULL
	ORDER BY
	rto.out_date_time DESC