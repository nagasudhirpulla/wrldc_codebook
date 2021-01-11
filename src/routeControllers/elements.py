from src.security.decorators import roles_required
from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.repos.elements.elementsRepo import ElementsRepo
from src.appConfig import getConfig
from typing import List


elementsPage = Blueprint('elements', __name__,
                         template_folder='templates')


@elementsPage.route('/api/getElementTypes', methods=['GET'])
@roles_required(['code_book_editor', 'code_book_viewer'])
def getElementTypes() -> dict:
    appConf = getConfig()
    eRepo = ElementsRepo(appConf['pwcDbConnStr'])
    elTypes = eRepo.getElementTypes()
    return {"elTypes": elTypes}


@elementsPage.route('/api/getElementsByType/<elType>', methods=['GET'])
@roles_required(['code_book_editor', 'code_book_viewer'])
def getElementsByType(elType: str) -> dict:
    elObjs: List[dict] = []
    appConf = getConfig()
    eRepo = ElementsRepo(appConf['pwcDbConnStr'])
    if elType == 'Bay':
        bays = eRepo.getBaysForDisplay()
        elObjs = bays
    if elType == 'AC_TRANSMISSION_LINE_CIRCUIT':
        elems = eRepo.getTranLineCktsForDisplay()
        elObjs = elems
    return {"elements": elObjs}
