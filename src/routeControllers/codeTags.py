from flask import Blueprint, render_template, request, flash, redirect, url_for
from wtforms import Form, StringField, validators
from src.repos.codeTags.codeTagsRepo import CodeTagsRepo
from src.appConfig import getConfig
from src.security.decorators import roles_required, role_required

codeTagsPage = Blueprint('codeTags', __name__,
                         template_folder='templates')


@codeTagsPage.route('/api/all', methods=['GET'])
@roles_required(['code_book_editor', 'code_book_viewer'])
def getCodeTags():
    appConf = getConfig()
    cTagsRepo = CodeTagsRepo(appConf['appDbConnStr'])
    codeTags = cTagsRepo.getAllCodeTags()
    return {"codeTags": [x['tag'] for x in codeTags]}


@codeTagsPage.route('/', methods=['GET'])
@roles_required(['code_book_editor', 'code_book_viewer'])
def list():
    appConf = getConfig()
    cTagsRepo = CodeTagsRepo(appConf['appDbConnStr'])
    codeTags = cTagsRepo.getAllCodeTags()
    return render_template('codeTag/list.html.j2', data={'codeTags': codeTags})


@codeTagsPage.route('/delete/<codeTagId>', methods=['GET', 'POST'])
@roles_required(['code_book_editor'])
def delete(codeTagId: int):
    appConf = getConfig()
    cTagsRepo = CodeTagsRepo(appConf['appDbConnStr'])
    codeTag = cTagsRepo.getCodeTagById(codeTagId)
    if request.method == 'POST':
        isSuccess = cTagsRepo.deleteCodeTag(codeTagId)
        if isSuccess:
            flash('Successfully deleted the code tag suggestion', category='success')
            return redirect(url_for('codeTags.list'))
        else:
            flash('Could not delete the code tag suggestion', category='error')
    return render_template('codeTag/delete.html.j2', data={'codeTag': codeTag})


class CreateCodeTagCodeForm(Form):
    codeTag = StringField(
        'Tag Name', validators=[validators.DataRequired(), validators.Length(min=0, max=100)])


@codeTagsPage.route('/create', methods=['GET', 'POST'])
@role_required('code_book_editor')
def create():
    form = CreateCodeTagCodeForm(request.form)
    if request.method == 'POST' and form.validate():
        appConf = getConfig()
        cTagsRepo = CodeTagsRepo(appConf['appDbConnStr'])
        # initialize new code tag string as None
        codeTagStr = None

        # attach placeholder to code only if form input is not None
        suppliedCodeStr = form.codeTag.data
        if (not suppliedCodeStr == None) and (not suppliedCodeStr.strip() == ""):
            codeTagStr = suppliedCodeStr

        # create code tag
        isSuccess = cTagsRepo.insertCodeTag(codeTagStr)
        if isSuccess:
            flash(
                'Successfully created the code tag - {0}'.format(form.codeTag.data), category='success')
            return redirect(url_for('codeTags.list'))
        else:
            flash(
                'Could not create the code tag - {0}'.format(form.codeTag.data), category='danger')
    return render_template('codeTag/create.html.j2', form=form)
