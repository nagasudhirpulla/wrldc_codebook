from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from wtforms import Form, StringField, validators, DateTimeField, BooleanField, IntegerField
from wtforms.fields import html5 as h5fields
from wtforms.widgets import html5 as h5widgets
from wtforms.widgets import TextArea
from src.repos.codes.codesRepo import CodesRepo
from src.appConfig import getConfig
from src.security.decorators import role_required
from src.app.utils.getNewCodePlaceHolder import getNewCodePlaceHolder

elementRevivalCodePage = Blueprint('elementRevivalCode', __name__,
                                   template_folder='templates')


class CreateElementRevivalCodeForm(Form):
    code = StringField(
        'Code', validators=[validators.DataRequired(), validators.Length(min=1, max=100)])
    otherLdcCodes = StringField(
        'Other LDC Codes', [validators.Length(min=0, max=150)])
    codeDescription = StringField(
        'Description', validators=[validators.DataRequired(), validators.Length(min=1, max=500)], widget=TextArea())
    codeTags = StringField('Tags', [validators.Length(min=0, max=500)])
    codeIssuedTo = StringField(
        'Issued To', [validators.DataRequired(), validators.Length(min=1, max=500)])
    rtoId = h5fields.IntegerField(
        '', widget=h5widgets.NumberInput(min=0, step=1),
        validators=[validators.DataRequired()]
    )
    elementId = h5fields.IntegerField(
        '', widget=h5widgets.NumberInput(min=0, step=1),
        validators=[validators.DataRequired()]
    )
    elementTypeId = h5fields.IntegerField(
        '', widget=h5widgets.NumberInput(min=0, step=1),
        validators=[validators.DataRequired()]
    )
    elementName = StringField(
        '',
        validators=[validators.DataRequired(), validators.Length(min=1, max=500)])
    elementType = StringField(
        '',
        validators=[validators.DataRequired(), validators.Length(min=1, max=250)])


@elementRevivalCodePage.route('/create', methods=['GET', 'POST'])
@role_required('code_book_editor')
def create():
    form = CreateElementRevivalCodeForm(request.form)
    appConf = getConfig()
    if request.method == 'POST' and form.validate():
        cRepo = CodesRepo(appConf['appDbConnStr'])
        loggedInUsername = session['SUSER']['name']
        isSuccess = cRepo.insertElementRevivalCode(
            code_issue_time=None, code_str=getNewCodePlaceHolder()+form.code.data, other_ldc_codes=form.otherLdcCodes.data,
            code_description=form.codeDescription.data, code_execution_time=None,
            code_tags=form.codeTags.data, code_issued_by=loggedInUsername, code_issued_to=form.codeIssuedTo.data,
            pwc_element_type_id=form.elementTypeId.data, pwc_element_id=form.elementId.data,
            pwc_element_name=form.elementName.data, pwc_element_type=form.elementType.data,
            pwc_rto_id=form.rtoId.data)
        if isSuccess:
            flash(
                'Successfully created the revival code - {0}'.format(form.code.data), category='success')
            return redirect(url_for('codes.list'))
        else:
            flash(
                'Could not create the revival code - {0}, please check if element is already in service'.format(form.code.data), category='danger')
    return render_template('elementRevivalCode/create.html.j2', form=form)
