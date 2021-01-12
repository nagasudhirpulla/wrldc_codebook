/*
get outage tags for real time outage
In UI the relavent tags for outage type will be loaded based upon the user selection of shutdown outage type
*/
SELECT
	SD_TAG.ID,
	SD_TAG.NAME,
	SD_TAG.SHUTDOWN_OUTAGE_TYPE_ID
FROM
	REPORTING_WEB_UI_UAT.SHUTDOWN_OUTAGE_TAG SD_TAG
LEFT JOIN REPORTING_WEB_UI_UAT.SHUTDOWN_OUTAGE_TYPE SD_TYPE ON
	SD_TYPE.ID = SD_TAG.SHUTDOWN_OUTAGE_TYPE_ID
WHERE
	SD_TYPE.IS_APPROVED = 0
