from src.security.decorators import roles_required
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from src.repos.outages.outagesRepo import OutagesRepo
from src.appConfig import getConfig
from typing import List
import datetime as dt

outagesPage = Blueprint('outages', __name__,
                        template_folder='templates')


@outagesPage.route('/api/latestUnrevivedOutages', methods=['GET'])
@roles_required(['code_book_editor', 'code_book_viewer'])
def getLatestUnrevivedOutages() -> dict:
    appConf = getConfig()
    oRepo = OutagesRepo(appConf['pwcDbConnStr'])
    outages = oRepo.getLatestUnrevOutages()
    return jsonify({"outages": outages})


@outagesPage.route('/api/todayApprovedOutages', methods=['GET'])
@roles_required(['code_book_editor', 'code_book_viewer'])
def getApprovedOutages() -> dict:
    appConf = getConfig()
    oRepo = OutagesRepo(appConf['pwcDbConnStr'])
    outages = oRepo.getApprovedOutages(dt.datetime.now())
    return jsonify({"outages": outages})
