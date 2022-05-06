from types import CodeType
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from wtforms import Form, StringField, validators, DateTimeField, BooleanField, IntegerField
from wtforms.fields import html5 as h5fields
from wtforms.widgets import html5 as h5widgets
from wtforms.widgets import TextArea
from src.repos.elements.elementsRepo import ElementsRepo
from src.repos.codes.codesRepo import CodesRepo
from src.repos.outageTags.outageTagsRepo import OutageTagsRepo
from src.repos.outageTypes.outageTypesRepo import OutageTypesRepo
from src.appConfig import getConfig
from src.security.decorators import role_required
from src.app.utils.getNewCodePlaceHolder import getNewCodePlaceHolder

codeRequestPage = Blueprint('codeRequest', __name__,
                                   template_folder='templates')


class CreateCodeRequestForm(Form):
    code = StringField(
        'Code (Optional)', validators=[validators.Length(min=0, max=100)])
    otherLdcCodes = StringField(
        'Other LDC Codes', [validators.Length(min=0, max=150)])
    codeDescription = StringField(
        'Description', validators=[validators.DataRequired(), validators.Length(min=1, max=500)], widget=TextArea())
    codeType = StringField(
        'Code Type', [validators.DataRequired(), validators.Length(min=1, max=500)])
    codeTags = StringField('Tag(s)', [validators.Length(min=0, max=500)])
    codeIssuedTo = StringField(
        'Issued To', [validators.DataRequired(), validators.Length(min=1, max=500)])
    codeIssueTime = DateTimeField(
        'Issue Time (Optional)', format='%Y-%m-%d %H:%M', validators=[validators.Optional()])
    elementId = h5fields.IntegerField(
        '', widget=h5widgets.NumberInput(min=0, step=1),
        validators=[validators.DataRequired()]
    )
    elementTypeId = h5fields.IntegerField(
        '', widget=h5widgets.NumberInput(min=0, step=1),
        validators=[validators.DataRequired()]
    )
    outageTypeId = h5fields.IntegerField(
        '', widget=h5widgets.NumberInput(min=0, step=1),
        validators=[validators.DataRequired()]
    )
    outageTagId = h5fields.IntegerField(
        '', widget=h5widgets.NumberInput(min=0, step=1),
        validators=[validators.DataRequired()]
    )
    outageType = StringField(
        '',
        validators=[validators.DataRequired(), validators.Length(min=1, max=250)])
    outageTag = StringField(
        '',
        validators=[validators.DataRequired(), validators.Length(min=1, max=250)])
    elementName = StringField(
        '',
        validators=[validators.DataRequired(), validators.Length(min=1, max=500)])
    elementType = StringField(
        '',
        validators=[validators.DataRequired(), validators.Length(min=1, max=250)])
    sdReqId = h5fields.IntegerField(
        '', widget=h5widgets.NumberInput(min=0, step=1),
        validators=[]
    )


@codeRequestPage.route('/create', methods=['GET', 'POST'])
@role_required('code_book_editor')
def create():
    form = CreateCodeRequestForm(request.form)
    appConf = getConfig()
    oTagsRepo = OutageTagsRepo(appConf['pwcDbConnStr'])
    oTypesRepo = OutageTypesRepo(appConf['pwcDbConnStr'])
    oTags = oTagsRepo.getRealTimeOutageTags()
    oTypes = oTypesRepo.getRealTimeOutageTypes()
    if request.method == 'POST' and form.validate():
        cRepo = CodesRepo(appConf['appDbConnStr'])
        loggedInUsername = session['SUSER']['name']
        
        # initialize new code as None
        codeStr = None

        # attach placeholder to code only if form input is not None
        suppliedCodeStr = form.code.data
        if (not suppliedCodeStr == None) and (not suppliedCodeStr.strip() == ""):
            codeStr = getNewCodePlaceHolder()+suppliedCodeStr

        # create approved outage code
        if form.codeType == "OUTAGE":
            isSuccess = cRepo.insertElementOutageCode(
            code_issue_time=form.codeIssueTime.data, code_str=codeStr, other_ldc_codes=form.otherLdcCodes.data,
            code_description=form.codeDescription.data, code_execution_time=None,
            code_tags=form.codeTags.data, code_issued_by=loggedInUsername, code_issued_to=form.codeIssuedTo.data,
            pwc_element_type_id=form.elementTypeId.data, pwc_element_id=form.elementId.data,
            pwc_element_name=form.elementName.data, pwc_element_type=form.elementType.data,
            pwc_outage_type_id=form.outageTypeId.data, pwc_outage_tag_id=form.outageTagId.data,
            pwc_outage_type=form.outageType.data, pwc_outage_tag=form.outageTag.data)

        elif form.codeType == "APPROVED_OUTAGE":
            isSuccess = cRepo.insertApprovedOutageCode(
            code_issue_time=form.codeIssueTime.data, code_str=codeStr, other_ldc_codes=form.otherLdcCodes.data,
            code_description=form.codeDescription.data, code_execution_time=None,
            code_tags=form.codeTags.data, code_issued_by=loggedInUsername, code_issued_to=form.codeIssuedTo.data,
            pwc_element_type_id=form.elementTypeId.data, pwc_element_id=form.elementId.data,
            pwc_element_name=form.elementName.data, pwc_element_type=form.elementType.data,
            pwc_outage_type_id=form.outageTypeId.data, pwc_outage_tag_id=form.outageTagId.data,
            pwc_outage_type=form.outageType.data, pwc_outage_tag=form.outageTag.data, pwc_sd_req_id=form.sdReqId.data)

        elif form.codeType == "REVIVAL":
            isSuccess = cRepo.insertElementRevivalCode(
            code_issue_time=form.codeIssueTime.data, code_str=codeStr, other_ldc_codes=form.otherLdcCodes.data,
            code_description=form.codeDescription.data, code_execution_time=None,
            code_tags=form.codeTags.data, code_issued_by=loggedInUsername, code_issued_to=form.codeIssuedTo.data,
            pwc_element_type_id=form.elementTypeId.data, pwc_element_id=form.elementId.data,
            pwc_element_name=form.elementName.data, pwc_element_type=form.elementType.data,
            pwc_rto_id=form.rtoId.data)
        
        if isSuccess:
            flash(
                'Successfully created the approved outage code - {0}'.format(form.code.data), category='success')
            return redirect(url_for('codes.list'))
        else:
            flash(
                'Could not create the approved outage code - {0}, please check if element is already out'.format(form.code.data), category='danger')
    return render_template('codeRequest/create.html.j2', form=form, data={"oTags": oTags, "oTypes": oTypes})
