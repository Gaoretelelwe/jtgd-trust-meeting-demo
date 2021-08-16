from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, TextAreaField, RadioField, FileField, SubmitField
from wtforms.fields.html5 import DateField, DateTimeField, DateTimeLocalField
from wtforms.validators import InputRequired, Email, Length, EqualTo

from Util.FormField import FormField

import pdb #debugging tool -- pdb.set_trace()  

class HomeForm(FlaskForm):

    RequireLoginInd = False
    AdministratorForm = False
    
    username = StringField('Email', validators=[InputRequired(), Length(min=4, max=250), Email(message='Invalid email.')])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=15)])
    remember = BooleanField('Remember me')


class WelcomeForm(FlaskForm):
    ff = FormField()

    RequireLoginInd = True
    AdministratorForm = False
    
class UserForm(FlaskForm):
    ff = FormField()
    
    RequireLoginInd = True
    AdministratorForm = True

    userFirstname = StringField('Firstname', validators=[InputRequired(), Length(min=2, max=50)])
    userLastname = StringField('Surname', validators=[InputRequired(), Length(min=2, max=50)])
    userEmail = StringField('Email', validators=[InputRequired(), Length(min=2, max=50)])
    
    agmInd = BooleanField('AGM')
    boardUserInd = BooleanField('BOARD USER')
    financeAuditRiskInd = BooleanField('FINANCE AUDIT RISK')
    projectReviewCommitteeInd = BooleanField('PROJECT REVIEW COMMITTEE')
    remcoInd = BooleanField('REMCO')
    
    userSave = SubmitField('Save User')
    
class MeetingForm(FlaskForm):
    ff = FormField()
    
    RequireLoginInd = True
    AdministratorForm = False
    
    meetingType = SelectField('Meeting Type', choices=ff.get_MeetingTypes(), coerce=int)
    meetingTitle = StringField('Title', validators=[InputRequired(), Length(min=2, max=50)])
    #meetingStartDate = DateField('Start Date', format='%Y-%m-%d', validators=[InputRequired()])
    #meetingEndDate = DateField('End Date', format='%Y-%m-%d', validators=[InputRequired()])
    meetingStartDate = DateTimeLocalField('Start Date', format='%Y-%m-%dT%H:%M', validators=[InputRequired()])
    meetingEndDate = DateTimeLocalField('End Date', format='%Y-%m-%dT%H:%M', validators=[InputRequired()])
    
    meetingOnlineLink = StringField('Online Link', validators=[Length(min=0, max=200)])
    meetingRoom = StringField('Room Number', validators=[Length(min=0, max=50)])
    meetingBuilding = StringField('Building Name', validators=[Length(min=0, max=50)])
    meetingStreet = StringField('Street', validators=[Length(min=0, max=50)])
    meetingTown = StringField('Town', validators=[Length(min=0, max=50)])

    agmInd = BooleanField('AGM')
    boardUserInd = BooleanField('BOARD USER')
    financeAuditRiskInd = BooleanField('FINANCE AUDIT RISK')
    projectReviewCommitteeInd = BooleanField('PROJECT REVIEW COMMITTEE')
    remcoInd = BooleanField('REMCO')
    
    meetingAdd = SubmitField('Save Meeting')
    
class FileForm(FlaskForm):
    ff = FormField()
    
    RequireLoginInd = True
    AdministratorForm = False
    
    fileName = StringField('FIle Name', validators=[InputRequired(), Length(min=2, max=50)])
    fileContent = FileField('Attach file')
    
    agmInd = BooleanField('AGM')
    boardUserInd = BooleanField('BOARD USER')
    financeAuditRiskInd = BooleanField('FINANCE AUDIT RISK')
    projectReviewCommitteeInd = BooleanField('PROJECT REVIEW COMMITTEE')
    remcoInd = BooleanField('REMCO')
    
    fileSave = SubmitField('Save File')

class RecoverPasswordForm(FlaskForm):

    RequireLoginInd = False
    AdministratorForm = False

    username = StringField('Email Address', validators=[InputRequired(), Email(message='Invalid email.')])

class ResetPasswordForm(FlaskForm):

    RequireLoginInd = False
    AdministratorForm = False

    newPassword = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=15), EqualTo('newConfirmPassword', message='Password does not match.')])
    newConfirmPassword = PasswordField('Repeat Password')

class ProfileForm(FlaskForm):

    RequireLoginInd = True
    AdministratorForm = False

    userFirstname = StringField('Firstname', validators=[InputRequired(), Length(min=2, max=50)])
    userLastname = StringField('Surname', validators=[InputRequired(), Length(min=2, max=50)])
    userEmail = StringField('Email', validators=[InputRequired(), Length(min=2, max=50)])

    newPassword = PasswordField('Update Password', validators=[Length(min=0, max=15), EqualTo('newConfirmPassword', message='Password does not match.')])
    newConfirmPassword = PasswordField('Repeat Password')
    
    userSave = SubmitField('Save Profile')
    
