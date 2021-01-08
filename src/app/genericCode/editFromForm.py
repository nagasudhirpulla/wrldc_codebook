from src.repos.codes.codesRepo import CodesRepo
from src.app.genericCode.editForm import EditGenericCodeForm


def editGenericCodeViaForm(codeId: int, cRepo: CodesRepo, form: EditGenericCodeForm):
    isSuccess = cRepo.editGenericCode(codeId=codeId,
                                      code_issue_time=form.codeIssueTime.data,
                                      code_str=form.code.data,
                                      other_ldc_codes=form.otherLdcCodes.data,
                                      code_description=form.codeDescription.data,
                                      code_execution_time=form.codeExecTime.data,
                                      code_tags=form.codeTags.data, code_issued_by=form.codeIssuedBy.data,
                                      code_issued_to=form.codeIssuedTo.data,
                                      is_code_cancelled=form.isCodeCancelled.data)
    return isSuccess
