from flask import Blueprint, render_template, request, redirect, url_for, flash
from wtforms import Form, StringField, validators, DateTimeField, BooleanField
from src.repos.elements.elementsRepo import ElementsRepo
from src.appConfig import getConfig
from src.security.decorators import role_required

elementCodePage = Blueprint('elementCode', __name__,
                            template_folder='templates')


class CreateElementCodeForm(Form):
    code = StringField(
        'Code', validators=[validators.DataRequired(), validators.Length(min=1, max=100)])
    otherLdcCodes = StringField(
        'Other LDC Codes', [validators.Length(min=0, max=150)])
    codeDescription = StringField(
        'Description', [validators.DataRequired(), validators.Length(min=1, max=500)])
    codeTags = StringField('Tags', [validators.Length(min=0, max=500)])
    codeIssuedTo = StringField(
        'Issued To', [validators.DataRequired(), validators.Length(min=1, max=500)])
    # codeExecDate = DateTimeField('Code Execution Date-Time', format='%Y-%m-%d %H:%M', validators=[
    #                              validators.DataRequired()])


@elementCodePage.route('/create', methods=['GET', 'POST'])
@role_required('code_book_editor')
def create():
    form = CreateElementCodeForm(request.form)
    if request.method == 'POST' and form.validate():
        return redirect(url_for('code.list'))
    return render_template('elementCode/create.html.j2', form=form)
