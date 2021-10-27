from flask import Blueprint
from src.repos.codes.codesRepo import CodesRepo
from src.appConfig import getConfig
from src.security.decorators import roles_required

codesTagsPage = Blueprint('codeTags', __name__,
                          template_folder='templates')


@codesTagsPage.route('/api/all', methods=['GET'])
@roles_required(['code_book_editor', 'code_book_viewer'])
def getCodeTags():
    appConf = getConfig()
    cRepo = CodesRepo(appConf['appDbConnStr'])
    codeTags = cRepo.getAllCodeTags()
    return {"codeTags": codeTags}
