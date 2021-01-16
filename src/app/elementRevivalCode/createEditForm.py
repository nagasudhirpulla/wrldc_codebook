from src.typeDefs.code import ICode
from src.app.elementRevivalCode.editForm import EditElementRevivalCodeForm


def createElementRevivalCodeEditForm(code: ICode):
    form = EditElementRevivalCodeForm()
    form.codeIssueTime.data = code["codeIssueTime"]
    form.code.data = code["codeStr"]
    form.otherLdcCodes.data = code["otherLdcCodes"]
    form.codeIssuedTo.data = code["codeIssuedTo"]
    form.codeDescription.data = code["codeDesc"]
    form.codeExecTime.data = code["codeExecTime"]
    form.codeIssuedBy.data = code["codeIssuedBy"]
    form.codeTags.data = code["codeTags"]
    form.isCodeCancelled.data = False if code["isCodeCancelled"] == 0 else True
    form.rtoId.data = code["pwcRtoId"]
    return form
