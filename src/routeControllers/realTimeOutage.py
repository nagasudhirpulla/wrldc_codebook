from flask import Blueprint, render_template, request, redirect, url_for, flash
from wtforms import Form, StringField, validators, DateTimeField
from wtforms.fields import html5 as h5fields
from wtforms.widgets import html5 as h5widgets
from wtforms.widgets import TextArea
from src.repos.outageTags.outageTagsRepo import OutageTagsRepo
from src.repos.outageTypes.outageTypesRepo import OutageTypesRepo
from src.appConfig import getConfig
from src.security.decorators import role_required
from src.app.externalOutages.createRealTimeOutage import createRealTimeOutage
from src.app.externalOutages.checkIfElementIsOut import checkIfElementIsOut

realTimeOutagePage = Blueprint('realTimeOutage', __name__,
                               template_folder='templates')


class CreateElementOutageCodeForm(Form):
    outageReason = StringField(
        'Description', validators=[validators.DataRequired(), validators.Length(min=1, max=500)], widget=TextArea())
    outageTime = DateTimeField(
        'Outage Time', format='%Y-%m-%d %H:%M', validators=[validators.DataRequired()])
    elementId = h5fields.IntegerField(
        '', widget=h5widgets.NumberInput(min=0, step=1),
        validators=[validators.DataRequired()]
    )
    elementTypeId = h5fields.IntegerField(
        '', widget=h5widgets.NumberInput(min=0, step=1),
        validators=[validators.DataRequired()]
    )
    outageTypeId = h5fields.IntegerField(
        '', widget=h5widgets.NumberInput(min=0, step=1),
        validators=[validators.DataRequired()]
    )
    outageTagId = h5fields.IntegerField(
        '', widget=h5widgets.NumberInput(min=0, step=1),
        validators=[validators.DataRequired()]
    )
    outageType = StringField(
        '',
        validators=[validators.DataRequired(), validators.Length(min=1, max=250)])
    outageTag = StringField(
        '',
        validators=[validators.DataRequired(), validators.Length(min=1, max=250)])
    elementName = StringField(
        '',
        validators=[validators.DataRequired(), validators.Length(min=1, max=500)])
    elementType = StringField(
        '',
        validators=[validators.DataRequired(), validators.Length(min=1, max=250)])


@realTimeOutagePage.route('/create', methods=['GET', 'POST'])
@role_required('code_book_editor')
def create():
    form = CreateElementOutageCodeForm(request.form)
    appConf = getConfig()
    pwcDbConnStr = appConf['pwcDbConnStr']
    oTagsRepo = OutageTagsRepo(pwcDbConnStr)
    oTypesRepo = OutageTypesRepo(pwcDbConnStr)
    oTags = oTagsRepo.getRealTimeOutageTags()
    oTypes = oTypesRepo.getRealTimeOutageTypes()
    if request.method == 'POST' and form.validate():
        elId = form.elementId.data
        elTypeId = form.elementTypeId.data
        elName = form.elementName.data
        # check if element is already out
        isElOut = checkIfElementIsOut(
            pwcDbConnStr=pwcDbConnStr, elId=elId, elTypeId=elTypeId)
        if isElOut:
            # element is already out, hence this is not a valid real time outage
            print("could not edit element outage code for element {0} with element id = {1}, element type id = {2}, since element is already out".format(
                elName, elId, elTypeId))
            flash(
                'element already out, hence could not create the real-time outage', category='danger')
        else:
            # create real time outage
            newRtoId = createRealTimeOutage(
                pwcDbConnStr=pwcDbConnStr, elemTypeId=elTypeId,
                elementId=elId, outageDt=form.outageTime.data, outageTypeId=form.outageTypeId.data,
                reason=form.outageReason.data, elementName=form.elementName.data, sdReqId=0,
                outageTagId=form.outageTagId.data)
            if newRtoId > 0:
                flash(
                    'Successfully created the real-time outage with id - {0}'.format(newRtoId), category='success')
                # return redirect(url_for('codes.list'))
            else:
                flash('Could not create the real-time outage', category='danger')
    return render_template('realTimeOutage/create.html.j2', form=form, data={"oTags": oTags, "oTypes": oTypes})
