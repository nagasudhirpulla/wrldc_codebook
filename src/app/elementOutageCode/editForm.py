from wtforms import Form, StringField, validators, DateTimeField, BooleanField, IntegerField
from wtforms.fields import html5 as h5fields
from wtforms.widgets import html5 as h5widgets
from wtforms.widgets import TextArea


class EditElementOutageCodeForm(Form):
    codeIssueTime = DateTimeField('Code Issued Time', format='%Y-%m-%d %H:%M', validators=[
        validators.DataRequired()])
    code = StringField(
        'Code', validators=[validators.DataRequired(), validators.Length(min=1, max=100)])
    otherLdcCodes = StringField(
        'Other LDC Codes', [validators.Length(min=0, max=150)])
    codeDescription = StringField(
        'Description', [validators.DataRequired(), validators.Length(min=1, max=500)])
    codeTags = StringField('Tags', [validators.Length(min=0, max=500)])
    codeIssuedTo = StringField(
        'Issued To', [validators.DataRequired(), validators.Length(min=1, max=500)])
    codeExecTime = DateTimeField(
        'Execution Time', format='%Y-%m-%d %H:%M', validators=[validators.Optional()])
    codeIssuedBy = StringField(
        'Code Issued By', validators=[validators.DataRequired(),validators.Length(min=0, max=500)])
    isCodeCancelled = BooleanField("Code Cancelled")
    outageTypeId = h5fields.IntegerField(
        '', validators=[validators.DataRequired(), validators.NumberRange(min=0, max=100000)]
    )
    outageTagId = h5fields.IntegerField(
        '', validators=[validators.DataRequired(), validators.NumberRange(min=0, max=100000)]
    )
    outageType = StringField(
        '',
        validators=[validators.DataRequired(), validators.Length(min=1, max=250)])
    outageTag = StringField(
        '',
        validators=[validators.DataRequired(), validators.Length(min=1, max=250)])
