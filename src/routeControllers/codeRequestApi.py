from src.security.decorators import roles_required
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from src.repos.outages.outagesRepo import OutagesRepo
from src.app.outages.getLatestUnrevOutages import getLatestUnrevOutages
from src.appConfig import getConfig
from src.services.codeRequestApiHandler import CodeRequestApiHandler
from typing import List
import requests 
from wtforms import Form, StringField, validators, DateTimeField
import datetime as dt

codeRequestApiPage = Blueprint('codeRequestApi', __name__,
                        template_folder='templates')


@codeRequestApiPage.route('/api/latestUnrevivedOutages', methods=['GET'])
@roles_required(['code_book_editor', 'code_book_viewer'])
def getLatestUnrevivedOutages() -> dict:
    appConf = getConfig()
    outages = getLatestUnrevOutages(appConf['appDbConnStr'], appConf['pwcDbConnStr'])
    return jsonify({"outages": outages})


@codeRequestApiPage.route('/api/pendingCodeRequests', methods=['GET'])
@roles_required(['code_book_editor', 'code_book_viewer'])
def getCodeRequests() -> dict:
    appConf = getConfig()
    url = appConf['code_request_url']
    outageCodes = CodeRequestApiHandler(url)
    # payload = {'startDt': '2022-03-01', 'endDt': '2022-04-28'}
        
    # Api using APiHandler starts
    startDate = '2022-01-03'
    endDate = '2022-03-10'
    startDt = dt.datetime.strptime(startDate, '%Y-%m-%d')
    endDt = dt.datetime.strptime(endDate, '%Y-%m-%d')
    # print("API Handler")
    resp = outageCodes.getCodeRequest(startDt, endDt)
    # print(resp)
    # Api using APiHandler ends

    return resp
