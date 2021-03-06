SELECT
	b.id,
	b.BAY_NAME,
	b.BAY_NUMBER ,
	as2.SUBSTATION_NAME,
	bt.type,
	vol.TRANS_ELEMENT_TYPE AS voltage
FROM
	REPORTING_WEB_UI_UAT.BAY b
LEFT JOIN REPORTING_WEB_UI_UAT.BAY_TYPE bt ON
	bt.ID = b.BAY_TYPE_ID
LEFT JOIN REPORTING_WEB_UI_UAT.ASSOCIATE_SUBSTATION as2 ON
	as2.ID = b.STATION_ID
LEFT JOIN REPORTING_WEB_UI_UAT.TRANS_ELEMENT_TYPE_MASTER vol ON
	vol.TRANS_ELEMENT_TYPE_ID = b.VOLTAGE_ID