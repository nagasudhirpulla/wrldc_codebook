CREATE OR REPLACE
TRIGGER on_rto_deletion BEFORE
DELETE
	ON
	reporting_web_ui_uat.REAL_TIME_OUTAGE FOR EACH ROW
BEGIN
		INSERT
	INTO
	reporting_web_ui_uat.DELETED_OUTAGES (id)
VALUES(:OLD.ID);
END;