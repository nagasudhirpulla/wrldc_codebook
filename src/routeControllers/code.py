from flask import Blueprint, render_template, request, redirect, url_for, flash
from wtforms import Form, StringField, validators, DateTimeField
from src.repos.codes.codesRepo import CodesRepo
from src.appConfig import getConfig
from src.security.decorators import roles_required
import datetime as dt
from src.app.genericCode.editForm import EditGenericCodeForm
from src.app.genericCode.editFromForm import editGenericCodeViaForm
from src.app.genericCode.createEditForm import createGenericCodeEditForm
from src.app.elementCode.editForm import EditElementCodeForm
from src.app.elementCode.editFromForm import editElementCodeViaForm
from src.app.elementCode.createEditForm import createElementCodeEditForm
from src.app.elementOutageCode.editForm import EditElementOutageCodeForm
from src.app.elementOutageCode.editFromForm import editElementOutageCodeViaForm
from src.app.elementOutageCode.createEditForm import createElementOutageCodeEditForm
from src.app.elementRevivalCode.editForm import EditElementRevivalCodeForm
from src.app.elementRevivalCode.editFromForm import editElementRevivalCodeViaForm
from src.app.elementRevivalCode.createEditForm import createElementRevivalCodeEditForm
from src.repos.outageTags.outageTagsRepo import OutageTagsRepo
from src.repos.outageTypes.outageTypesRepo import OutageTypesRepo
import werkzeug
import json
from src.app.utils.defaultJsonEncoder import defaultJsonEncoder

codesPage = Blueprint('codes', __name__,
                     template_folder='templates')


class ListCodesForm(Form):
    startDate = DateTimeField('Start date', format='%Y-%m-%d', validators=[
        validators.DataRequired()])
    endDate = DateTimeField('End date', format='%Y-%m-%d', validators=[
        validators.DataRequired()])


@codesPage.route('/api/latest', methods=['GET'])
@roles_required(['code_book_editor', 'code_book_viewer'])
def getLatestCode():
    form = ListCodesForm(request.form)
    appConf = getConfig()
    cRepo = CodesRepo(appConf['appDbConnStr'])
    latestCode = cRepo.getLatestCode()
    return {"code": latestCode}


@codesPage.route('/', methods=['GET', 'POST'])
@roles_required(['code_book_editor', 'code_book_viewer'])
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


@codesPage.route('/delete/<codeId>', methods=['GET', 'POST'])
@roles_required(['code_book_editor'])
def delete(codeId: int):
    appConf = getConfig()
    cRepo = CodesRepo(appConf['appDbConnStr'])
    if request.method == 'POST':
        isSuccess = cRepo.deleteCode(codeId)
        if isSuccess:
            flash('Successfully deleted the code', category='success')
            return redirect(url_for('codes.list'))
        else:
            flash('Could not delete the code', category='error')
    else:
        code = cRepo.getCodeById(codeId)
    return render_template('code/delete.html.j2', data={'code': code})


@codesPage.route('/edit/<codeId>', methods=['GET', 'POST'])
@roles_required(['code_book_editor'])
def edit(codeId: int):
    appConf = getConfig()
    cRepo = CodesRepo(appConf['appDbConnStr'])
    code = cRepo.getCodeById(codeId)
    if code == None:
        raise werkzeug.exceptions.NotFound()
    if code["codeType"] == "Generic":
        if request.method == 'POST':
            form = EditGenericCodeForm(request.form)
            if form.validate():
                isSuccess = editGenericCodeViaForm(
                    codeId=codeId, cRepo=cRepo, form=form)
                if isSuccess:
                    flash(
                        'Successfully edited the code - {0}'.format(form.code.data), category='success')
                else:
                    flash(
                        'Could not edit the code - {0}'.format(form.code.data), category='danger')
                return redirect(url_for('codes.list'))
        else:
            form = createGenericCodeEditForm(code)
        return render_template('genericCode/edit.html.j2', form=form)
    elif code["codeType"] == "Element":
        if request.method == 'POST':
            form = EditElementCodeForm(request.form)
            if form.validate():
                isSuccess = editElementCodeViaForm(
                    codeId=codeId, cRepo=cRepo, form=form)
                if isSuccess:
                    flash(
                        'Successfully edited the code - {0}'.format(form.code.data), category='success')
                else:
                    flash(
                        'Could not edit the code - {0}'.format(form.code.data), category='danger')
                return redirect(url_for('codes.list'))
        else:
            form = createElementCodeEditForm(code)
        return render_template('elementCode/edit.html.j2', form=form)
    elif code["codeType"] == "Outage":
        if request.method == 'POST':
            form = EditElementOutageCodeForm(request.form)
            if form.validate():
                isSuccess = editElementOutageCodeViaForm(
                    codeId=codeId, cRepo=cRepo, form=form)
                if isSuccess:
                    flash(
                        'Successfully edited the code - {0}'.format(form.code.data), category='success')
                else:
                    flash(
                        'Could not edit the code - {0}, please check if element is already out'.format(form.code.data), category='danger')
                return redirect(url_for('codes.list'))
        else:
            form = createElementOutageCodeEditForm(code)
        oTagsRepo = OutageTagsRepo(appConf['pwcDbConnStr'])
        oTypesRepo = OutageTypesRepo(appConf['pwcDbConnStr'])
        oTags = oTagsRepo.getRealTimeOutageTags()
        oTypes = oTypesRepo.getRealTimeOutageTypes()
        return render_template('elementOutageCode/edit.html.j2', form=form,
                               data={"code": json.dumps(code, default=defaultJsonEncoder), "oTags": oTags, "oTypes": oTypes})
    elif code["codeType"] == "Revival":
        if request.method == 'POST':
            form = EditElementRevivalCodeForm(request.form)
            if form.validate():
                isSuccess = editElementRevivalCodeViaForm(
                    codeId=codeId, cRepo=cRepo, form=form)
                if isSuccess:
                    flash(
                        'Successfully edited the code - {0}'.format(form.code.data), category='success')
                else:
                    flash(
                        'Could not edit the code - {0}, please check if element is already in service'.format(form.code.data), category='danger')
                return redirect(url_for('codes.list'))
        else:
            form = createElementRevivalCodeEditForm(code)
        return render_template('elementRevivalCode/edit.html.j2', form=form,
                               data={"code": json.dumps(code, default=defaultJsonEncoder)})
    else:
        raise werkzeug.exceptions.NotFound()
