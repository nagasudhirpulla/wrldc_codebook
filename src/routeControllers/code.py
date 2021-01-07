from flask import Blueprint, render_template, request, redirect, url_for, flash
from wtforms import Form, StringField, validators, DateTimeField
from src.repos.codes.codesRepo import CodesRepo
from src.appConfig import getConfig
from src.security.decorators import roles_required
import datetime as dt

codePage = Blueprint('code', __name__,
                     template_folder='templates')


class ListCodesForm(Form):
    startDate = DateTimeField('Start date', format='%Y-%m-%d', validators=[
        validators.DataRequired()])
    endDate = DateTimeField('End date', format='%Y-%m-%d', validators=[
        validators.DataRequired()])


@codePage.route('/', methods=['GET', 'POST'])
# @roles_required(['code_book_editor', 'code_book_viewer'])
def list():
    form = ListCodesForm(request.form)
    appConf = getConfig()
    cRepo = CodesRepo(appConf['appDbConnStr'])
    if request.method == 'POST' and form.validate():
        codes = cRepo.getCodesBetweenDates(
            startDt=form.startDate.data, endDt=form.endDate.data)
    else:
        todayDt = dt.datetime.now()
        codes = cRepo.getCodesBetweenDates(
            startDt=todayDt, endDt=todayDt)
    return render_template('code/list.html.j2', form=form, data={'codes': codes})

@codePage.route('/delete/<codeId>', methods=['GET', 'POST'])
@roles_required(['code_book_editor'])
def delete(codeId:int):
    appConf = getConfig()
    cRepo = CodesRepo(appConf['appDbConnStr'])
    if request.method == 'POST':
        isSuccess = cRepo.deleteCode(codeId)
        if isSuccess:
            flash('Successfully deleted the code', category='success')
            return redirect(url_for('code.list'))
        else:
            flash('Could not delete the code', category='error')
    else:
        code = cRepo.getCodeById(codeId)
    return render_template('code/delete.html.j2', data={'code': code})
