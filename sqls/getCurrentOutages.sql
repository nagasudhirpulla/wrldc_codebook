SELECT
	rto.*,
CASE
		WHEN rto.revived_date IS NULL THEN 'NO'
		ELSE 'YES'
	END IS_REVIVED
FROM
	(
	SELECT
		outages.*, ent_master.ENTITY_NAME, reas.reason, sd_type.name AS SHUT_DOWN_TYPE_NAME, sd_tag.name AS shutown_tag, to_char(outages.OUTAGE_DATE , 'YYYY-MM-DD')|| ' ' || outages.OUTAGE_TIME AS out_date_time
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
		element_id, entity_id, SHUT_DOWN_TYPE, MAX(to_char(OUTAGE_DATE , 'YYYY-MM-DD')|| ' ' || OUTAGE_TIME) AS out_date_time
	FROM
		reporting_web_ui_uat.REAL_TIME_OUTAGE
	GROUP BY
		entity_id, ELEMENT_ID, SHUT_DOWN_TYPE) latest_out_info ON
	((latest_out_info.entity_id = rto.entity_id)
	AND (latest_out_info.element_id = rto.element_id)
	AND (latest_out_info.SHUT_DOWN_TYPE = rto.SHUT_DOWN_TYPE)
	AND (latest_out_info.out_date_time = rto.out_date_time))