from src.typeDefs.code import ICode
from src.app.elementOutageCode.editForm import EditElementOutageCodeForm


def createElementOutageCodeEditForm(code: ICode):
    form = EditElementOutageCodeForm()
    form.codeIssueTime.data = code["codeIssueTime"]
    form.code.data = code["codeStr"]
    form.otherLdcCodes.data = code["otherLdcCodes"]
    form.codeIssuedTo.data = code["codeIssuedTo"]
    form.codeDescription.data = code["codeDesc"]
    form.codeExecTime.data = code["codeExecTime"]
    form.codeIssuedBy.data = code["codeIssuedBy"]
    form.codeTags.data = code["codeTags"]
    form.isCodeCancelled.data = False if code["isCodeCancelled"] == 0 else True
    form.outageTypeId.data = code["pwcOutageTypeId"]
    form.outageType.data = code["pwcOutageType"]
    form.outageTagId.data = code["pwcOutageTagId"]
    form.outageTag.data = code["pwcOutageTag"]
    return form
