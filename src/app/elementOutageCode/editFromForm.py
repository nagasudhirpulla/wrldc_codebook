from src.repos.codes.codesRepo import CodesRepo
from src.app.elementOutageCode.editForm import EditElementOutageCodeForm


def editElementOutageCodeViaForm(codeId: int, cRepo: CodesRepo, form: EditElementOutageCodeForm):
    isSuccess = cRepo.editElementOutageCode(codeId=codeId,
                                            code_issue_time=form.codeIssueTime.data,
                                            code_str=form.code.data,
                                            other_ldc_codes=form.otherLdcCodes.data,
                                            code_description=form.codeDescription.data,
                                            code_execution_time=form.codeExecTime.data,
                                            code_tags=form.codeTags.data, code_issued_by=form.codeIssuedBy.data,
                                            code_issued_to=form.codeIssuedTo.data,
                                            is_code_cancelled=form.isCodeCancelled.data,
                                            pwc_outage_type_id=form.outageTypeId, pwc_outage_tag_id=form.outageTagId,
                                            pwc_outage_type=form.outageType, pwc_outage_tag=form.outageTag)
    return isSuccess
