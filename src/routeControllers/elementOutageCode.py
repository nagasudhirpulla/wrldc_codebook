from flask import Blueprint, render_template, request, redirect, url_for, flash
from wtforms import Form, StringField, validators, DateTimeField, BooleanField, IntegerField
from wtforms.fields import html5 as h5fields
from wtforms.widgets import html5 as h5widgets
from src.repos.elements.elementsRepo import ElementsRepo
from src.repos.codes.codesRepo import CodesRepo
from src.appConfig import getConfig
from src.security.decorators import role_required

elementCodePage = Blueprint('elementOutageCode', __name__,
                            template_folder='templates')


class CreateElementOutageCodeForm(Form):
    code = StringField(
        'Code', validators=[validators.DataRequired(), validators.Length(min=1, max=100)])
    otherLdcCodes = StringField(
        'Other LDC Codes', [validators.Length(min=0, max=150)])
    codeDescription = StringField(
        'Description', [validators.DataRequired(), validators.Length(min=1, max=500)])
    codeTags = StringField('Tags', [validators.Length(min=0, max=500)])
    codeIssuedTo = StringField(
        'Issued To', [validators.DataRequired(), validators.Length(min=1, max=500)])
    elementId = h5fields.IntegerField(
        "Element Id", widget=h5widgets.NumberInput(min=0, step=1)
    )
    elementTypeId = h5fields.IntegerField(
        "Element Type Id", widget=h5widgets.NumberInput(min=0, step=1),
        validators=[validators.DataRequired()]
    )
    outageTypeId = h5fields.IntegerField(
        "Outage Type Id", widget=h5widgets.NumberInput(min=0, step=1),
        validators=[validators.DataRequired()]
    )
    outageTagId = h5fields.IntegerField(
        "Outage Tag Id", widget=h5widgets.NumberInput(min=0, step=1),
        validators=[validators.DataRequired()]
    )
    outageType = StringField(
        'Outage Type',
        validators=[validators.DataRequired(), validators.Length(min=1, max=250)])
    outageTag = StringField(
        'Outage Tag',
        validators=[validators.DataRequired(), validators.Length(min=1, max=250)])
    elementName = StringField(
        'Element Name',
        validators=[validators.DataRequired(), validators.Length(min=1, max=500)])
    elementType = StringField(
        'Element Type',
        validators=[validators.DataRequired(), validators.Length(min=1, max=250)])


@elementCodePage.route('/create', methods=['GET', 'POST'])
@role_required('code_book_editor')
def create():
    form = CreateElementOutageCodeForm(request.form)
    if request.method == 'POST' and form.validate():
        # TODO complete this
        appConf = getConfig()
        cRepo = CodesRepo(appConf['appDbConnStr'])
        isSuccess = cRepo.insertElementCode(
            code_issue_time=None, code_str=form.code.data, other_ldc_codes=form.otherLdcCodes.data,
            code_description=form.codeDescription.data, code_execution_time=None,
            code_tags=form.codeTags.data, code_issued_by="NA", code_issued_to=form.codeIssuedTo.data,
            pwc_element_type_id=form.elementTypeId.data, pwc_element_id=form.elementId.data,
            pwc_element_name=form.elementName.data, pwc_element_type=form.elementType.data)
        if isSuccess:
            flash(
                'Successfully created the element outage code - {0}'.format(form.code.data), category='success')
            return redirect(url_for('code.list'))
        else:
            flash(
                'Could not create the element outage code - {0}'.format(form.code.data), category='danger')
    return render_template('elementOutageCode/create.html.j2', form=form)
