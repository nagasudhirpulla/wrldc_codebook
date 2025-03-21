from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from wtforms import Form, StringField, validators, DateTimeField, BooleanField
from wtforms.widgets import TextArea
from src.repos.codes.codesRepo import CodesRepo
from src.appConfig import getConfig
from src.security.decorators import role_required
from src.app.utils.getNewCodePlaceHolder import getNewCodePlaceHolder
from src.utils.returnUri import redirectTo

genericCodePage = Blueprint('genericCode', __name__,
                            template_folder='templates')


class CreateGenericCodeForm(Form):
    code = StringField(
        'Code (Optional)', validators=[validators.Length(min=0, max=100)])
    otherLdcCodes = StringField(
        'Other LDC Codes', [validators.Length(min=0, max=150)])
    codeDescription = StringField(
        'Description', validators=[validators.DataRequired(), validators.Length(min=1, max=500)], widget=TextArea())
    codeTags = StringField('Tag(s)', [validators.Length(min=0, max=500)])
    codeIssuedTo = StringField(
        'Issued To', [validators.DataRequired(), validators.Length(min=1, max=500)])
    codeIssueTime = DateTimeField(
        'Issue Time (Optional)', format='%Y-%m-%d %H:%M', validators=[validators.Optional()])


@genericCodePage.route('/create', methods=['GET', 'POST'])
@role_required('code_book_editor')
def create():
    form = CreateGenericCodeForm(request.form)
    if request.method == 'POST' and form.validate():
        appConf = getConfig()
        cRepo = CodesRepo(appConf['appDbConnStr'])
        loggedInUsername = session['SUSER']['name']
        # loggedInUsername = 'wrldccr'

        # initialize new code as None
        codeStr = None

        # attach placeholder to code only if form input is not None
        suppliedCodeStr = form.code.data
        if (not suppliedCodeStr == None) and (not suppliedCodeStr.strip() == ""):
            codeStr = getNewCodePlaceHolder()+suppliedCodeStr

        # create generic code
        isSuccess = cRepo.insertGenericCode(
            code_issue_time=form.codeIssueTime.data, code_str=codeStr, other_ldc_codes=form.otherLdcCodes.data,
            code_description=form.codeDescription.data, code_execution_time=None,
            code_tags=form.codeTags.data, code_issued_by=loggedInUsername, code_issued_to=form.codeIssuedTo.data)
        if isSuccess:
            flash(
                'Successfully created the code - {0}'.format(form.code.data), category='success')
            return redirectTo(url_for('codes.list'))
        else:
            flash(
                'Could not create the code - {0}'.format(form.code.data), category='danger')
    return render_template('genericCode/create.html.j2', form=form)
