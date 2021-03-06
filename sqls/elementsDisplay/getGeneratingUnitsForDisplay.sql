SELECT
	gu.id,
	gu.UNIT_NAME,
	gu.UNIT_NUMBER,
	gu.INSTALLED_CAPACITY,
	gu.MVA_CAPACITY, 
	vol.TRANS_ELEMENT_TYPE AS generating_voltage
FROM
	REPORTING_WEB_UI_UAT.GENERATING_UNIT gu
LEFT JOIN REPORTING_WEB_UI_UAT.TRANS_ELEMENT_TYPE_MASTER vol ON
	vol.TRANS_ELEMENT_TYPE_ID = gu.GENERATING_VOLTAGE_KV