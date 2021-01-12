from flask import Blueprint, render_template, request, redirect, url_for, flash
from wtforms import Form, StringField, validators, DateTimeField, BooleanField
from wtforms.widgets import TextArea
from src.repos.codes.codesRepo import CodesRepo
from src.appConfig import getConfig
from src.security.decorators import role_required

genericCodePage = Blueprint('genericCode', __name__,
                            template_folder='templates')


class CreateGenericCodeForm(Form):
    code = StringField(
        'Code', validators=[validators.DataRequired(), validators.Length(min=1, max=100)])
    otherLdcCodes = StringField(
        'Other LDC Codes', [validators.Length(min=0, max=150)])
    codeDescription = StringField(
        'Description', validators=[validators.DataRequired(), validators.Length(min=1, max=500)], widget=TextArea())
    codeTags = StringField('Tags', [validators.Length(min=0, max=500)])
    codeIssuedTo = StringField(
        'Issued To', [validators.DataRequired(), validators.Length(min=1, max=500)])


@genericCodePage.route('/create', methods=['GET', 'POST'])
@role_required('code_book_editor')
def create():
    form = CreateGenericCodeForm(request.form)
    if request.method == 'POST' and form.validate():
        appConf = getConfig()
        cRepo = CodesRepo(appConf['appDbConnStr'])
        isSuccess = cRepo.insertGenericCode(
            code_issue_time=None, code_str=form.code.data, other_ldc_codes=form.otherLdcCodes.data,
            code_description=form.codeDescription.data, code_execution_time=None,
            code_tags=form.codeTags.data, code_issued_by="NA", code_issued_to=form.codeIssuedTo.data)
        if isSuccess:
            flash(
                'Successfully created the code - {0}'.format(form.code.data), category='success')
            return redirect(url_for('code.list'))
        else:
            flash(
                'Could not create the code - {0}'.format(form.code.data), category='danger')
    return render_template('genericCode/create.html.j2', form=form)
