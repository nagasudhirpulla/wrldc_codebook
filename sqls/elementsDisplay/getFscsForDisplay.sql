SELECT
	f.ID,
	f.FSC_NAME,
	as2.SUBSTATION_NAME
FROM
	REPORTING_WEB_UI_UAT.FSC f
LEFT JOIN REPORTING_WEB_UI_UAT.ASSOCIATE_SUBSTATION as2 ON
	as2.ID = f.FK_SUBSTATION
