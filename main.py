from flask import Flask, render_template, redirect, url_for, session, Response, g, request, make_response, flash, send_file
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_mail import Mail, Message

from wtforms import StringField, BooleanField, SelectField, TextAreaField, IntegerField, FloatField
from wtforms.validators import InputRequired, DataRequired, Length, EqualTo
from werkzeug.utils import escape, unescape, secure_filename

import uuid
import datetime
import os
import pdb  # debugging tool -- pdb.set_trace()

# <!-- style="{{ vendorShareholder.style }}"> -->

from DataAccess.DataAccess import DataAccess

from Objects.DataObjects.DatabaseObjects import AccessGroup, File, FileAccess, Location, Meeting, MeetingAccess, MeetingInvitation, MeetingType, User, UserAccessGroup, MeetingFile
from Objects.DataObjects.Session import Session

from Objects.Forms.AppForms import HomeForm, WelcomeForm, UserForm, MeetingForm, FileForm, RecoverPasswordForm, ResetPasswordForm, ProfileForm

from Util.Encryption import AESCipher
from Util.ErrorHandler import InsertError, UpdateError, DeleteError, LoginError, SelectionError, CaptureError, FileMissingError, FileSizeError, RecoverPasswordError, FetchError, ApplicationSubmissionError
from Util.Lists import Lists
from Util.LoginLogic import LoginLogic
from Util.RecoverPasswordLogic import RecoverPasswordLogic
from Util.StoredProcs import StoredProcs
from Util.PythonSQL import PythonSQL

from system_config import SystemConfig

from random import seed, randint

sysConfig = SystemConfig()

ALLOWED_EXTENSIONS = sysConfig.APP_ALLOWED_EXTENSION
TEMPLATE_FOLDER = sysConfig.APP_TEMPLATE_FOLDER

app = Flask(__name__, template_folder=TEMPLATE_FOLDER)
app.config['SECRET_KEY'] = sysConfig.APP_SECRET_KEY
app.config['UPLOAD_FOLDER'] = sysConfig.APP_UPLOAD_FOLDER
app.config['REPORTS_FOLDER'] = sysConfig.APP_UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = sysConfig.APP_MAX_CONTENT_LENGTH


#app.config.update(
#	MAIL_SERVER=sysConfig.REGISTRATION_MAIL_SERVER, 
#	MAIL_PORT=sysConfig.REGISTRATION_MAIL_PORT, 
#	MAIL_USE_SSL=True,
#	MAIL_USERNAME = sysConfig.REGISTRATION_MAIL_USERNAME, 
#	MAIL_PASSWORD = sysConfig.REGISTRATION_MAIL_PASSWORD 
#	)

app.config['NOTIFICATION_EMAIL_SENDER'] = sysConfig.NOTIFICATIONS_MAIL_SENDER
app.config['ACCOUNTS_EMAIL_SENDER'] = sysConfig.REGISTRATION_MAIL_SENDER
app.config.update(
	MAIL_SERVER=sysConfig.NOTIFICATIONS_MAIL_SERVER, 
	MAIL_PORT=sysConfig.NOTIFICATIONS_MAIL_PORT, 
	MAIL_USE_SSL=True,
	MAIL_USERNAME = sysConfig.NOTIFICATIONS_MAIL_USERNAME, 
	MAIL_PASSWORD = sysConfig.NOTIFICATIONS_MAIL_PASSWORD 
	)

Bootstrap(app)
mail = Mail(app)


@app.before_request
def before_request_func():
    
    g.data_access = DataAccess()
    g.data_access.begin_transaction()
    
    g.app_has_errors = False
    
    #if not request.is_secure and app.env != "development":
    #    url = request.url.replace("http://", "https://", 1)
    #    code = 301
    #    return redirect(url, code=code)

    # Session Create (Get)
    if not request.cookies.get('jtgd-trust-meeting-cookie'):
        sessionGuid = str(uuid.uuid4())
        createDate = datetime.datetime.now()
        lastAccessDate = createDate
        g.session = Session(SessionGuid=sessionGuid, CreateDate=createDate, LastAccessDate=lastAccessDate, UniqueAccessDays=0, data_access=g.data_access)
        g.session.Save()
        g.cookie_key = 'jtgd-trust-meeting-cookie'
        g.cookie_value = sessionGuid
    else:
        try:
            sessionGuid = request.cookies.get('jtgd-trust-meeting-cookie')
            g.session = Session(SessionGuid=sessionGuid, data_access=g.data_access)
            g.session.DBFetchGUID(sessionGuid)

            if g.session.LastAccessDate.date() != datetime.datetime.now().date():
                g.session.UniqueAccessDays = g.session.UniqueAccessDays + 1
                g.session.LastAccessDate = datetime.datetime.now()
                g.session.Save()

            if g.session.LoggedInInd == 1:
                loggedInUser = User(UserId=g.session.UserId, data_access=g.data_access)
                loggedInUser.DBFetch(g.session.UserId)
                g.loggedinEntityName = loggedInUser.Firstname + ' ' + loggedInUser.Lastname
            else:
                g.loggedinEntityName = ''

            g.cookie_key = 'jtgd-trust-meeting-cookie'
            g.cookie_value = sessionGuid

        except FetchError as fetch_error:
            sessionGuid = str(uuid.uuid4())
            createDate = datetime.datetime.now()
            lastAccessDate = createDate
            g.session = Session(SessionGuid=sessionGuid,
                                CreateDate=createDate,
                                LastAccessDate=lastAccessDate,
                                data_access=g.data_access)
            g.session.Save()
            g.cookie_key = 'jtgd-trust-meeting-cookie'
            g.cookie_value = sessionGuid
            flash(fetch_error.message, "danger")

    g.endpoint = request.endpoint
    g.url = request.url
    g.method = request.method
    g.domain_name = request.url_root


@app.after_request
def after_request_func(response):

    if g.app_has_errors:
        g.data_access.rollback_transaction()
    else:
        g.data_access.commit_transaction()
    
    g.data_access.close_connection()
    set_jtgd_trust_meeting_cookie(response, g.cookie_key, g.cookie_value)
    return response


def set_jtgd_trust_meeting_cookie(resp, key, guid):

    if g.session.RememberInd == 1:
        expire_date = datetime.datetime.now()
        # Cookie expires after seven days
        expire_date = expire_date + datetime.timedelta(days=7)
        resp.set_cookie(key, guid, expires=expire_date)
    else:
        resp.set_cookie(key, guid)

def redirect_to_home():
    form = HomeForm()
    
    resp = make_response(render_template('home.html', form=form))
    return resp

def _get_Admin_SideMenuItems():
    homeLink = str(g.domain_name) + str(url_for('welcome_view', sessionGuid=g.session.SessionGuid))[1:] 
    profileLink = str(g.domain_name) + str(url_for('profile_view', sessionGuid=g.session.SessionGuid))[1:] 
    pastMeetingsLink = str(g.domain_name) + str(url_for('pastmeetings_view', sessionGuid=g.session.SessionGuid))[1:] 
    manageMeetingsLink = str(g.domain_name) + str(url_for('managemeetings_view', sessionGuid=g.session.SessionGuid))[1:] 
    manageUsersLink = str(g.domain_name) + str(url_for('manageusers_view', sessionGuid=g.session.SessionGuid))[1:] 
    logoutLink = str(g.domain_name) + str(url_for('logout_view'))[1:] 

    sideMenuItems =[{"itemName":"Home", "link":homeLink},
                    {"itemName":"Profile", "link":profileLink},
                    {"itemName":"Past Meetings", "link":pastMeetingsLink},
                    {"itemName": "Manage Meetings", "link": manageMeetingsLink},
                    {"itemName": "Manage Users", "link": manageUsersLink},
                    {"itemName":"Logout", "link":logoutLink}]
    
    return sideMenuItems

def _get_Normal_SideMenuItems():
    homeLink = str(g.domain_name) + str(url_for('welcome_view', sessionGuid=g.session.SessionGuid))[1:] 
    profileLink = str(g.domain_name) + str(url_for('profile_view', sessionGuid=g.session.SessionGuid))[1:] 
    pastMeetingsLink = str(g.domain_name) + str(url_for('pastmeetings_view', sessionGuid=g.session.SessionGuid))[1:] 
    logoutLink = str(g.domain_name) + str(url_for('logout_view'))[1:] 

    sideMenuItems =[{"itemName":"Home", "link":homeLink},
                    {"itemName":"Profile", "link":profileLink},
                    {"itemName":"Past Meetings", "link":pastMeetingsLink},
                    {"itemName":"Logout", "link":logoutLink}]
    
    return sideMenuItems


@app.route('/send-mail', methods=['GET', 'POST'])
def send_mail():
    
    subject = "Send Mail Tutorial"
    sender = "gaoretelelwe@tuelopay.co.za"
    recipients = ["molebalwag@yahoo.co.uk"]
    body = "Yo!\nHave you heard the good word of Python???"
    SendEmail(subject=subject, sender=sender, recipients=recipients, body=body)
    SendNotificationEmail(subject=subject, sender=sender, recipients=recipients, body=body)
    SendRegistrationEmail(subject=subject, sender=sender, recipients=recipients, body=body)
    SendNotificationEmail(subject=subject, sender=sender, recipients=recipients, body=body)
    SendEmail(subject=subject, sender=sender, recipients=recipients, body=body)
    return 'Mail sent!'
	

def SendEmail(subject, sender, recipients, body):

    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = body

    mail.send(msg)

def SendNotificationEmail(subject, sender, recipients, body):
    app.config.update(
        MAIL_SERVER=sysConfig.NOTIFICATIONS_MAIL_SERVER, 
        MAIL_PORT=sysConfig.NOTIFICATIONS_MAIL_PORT, 
        MAIL_USE_SSL=True,
        MAIL_USERNAME = sysConfig.NOTIFICATIONS_MAIL_USERNAME, 
        MAIL_PASSWORD = sysConfig.NOTIFICATIONS_MAIL_PASSWORD 
        )
    mail = Mail(app)
    SendEmail(subject=subject, sender=sender, recipients=recipients, body=body)
    _set_Default_Mail_Server()

def SendRegistrationEmail(subject, sender, recipients, body):
    app.config.update(
        MAIL_SERVER=sysConfig.REGISTRATION_MAIL_SERVER, 
        MAIL_PORT=sysConfig.REGISTRATION_MAIL_PORT, 
        MAIL_USE_SSL=True,
        MAIL_USERNAME = sysConfig.REGISTRATION_MAIL_USERNAME, 
        MAIL_PASSWORD = sysConfig.REGISTRATION_MAIL_PASSWORD 
        )
    mail = Mail(app)
    SendEmail(subject=subject, sender=sender, recipients=recipients, body=body)
    _set_Default_Mail_Server()

def _set_Default_Mail_Server():
    app.config.update(
        MAIL_SERVER=sysConfig.REGISTRATION_MAIL_SERVER, 
        MAIL_PORT=sysConfig.REGISTRATION_MAIL_PORT, 
        MAIL_USE_SSL=True,
        MAIL_USERNAME = sysConfig.REGISTRATION_MAIL_USERNAME, 
        MAIL_PASSWORD = sysConfig.REGISTRATION_MAIL_PASSWORD 
        )
    mail = Mail(app)


@app.route("/", methods=['GET', 'POST'])
def home_view(): 
    form = HomeForm()
    form_url = ('home.html')

    if form.RequireLoginInd and g.session.LoggedInInd != 1:
        clear_session_variables()
        return redirect(url_for('home_view'))

    if form.AdministratorForm and g.session.AdminInd != 1:
        clear_session_variables()
        return redirect(url_for('home_view'))

    if form.validate_on_submit():
        try:
            loginEmailAddress = form.username.data
            loginPassword = form.password.data

            remember = form.remember.data
            if remember: rememberInd = 1 
            else: rememberInd = 0
            
            loginLogic = LoginLogic(loginEmailAddress, loginPassword, g.data_access)
            loginLogic.Login()
            
            # Clear all Session 
            clear_session_variables()

            # Update RememberInd after clearing all variables
            g.session.RememberInd = rememberInd
            
            if loginLogic.IsLogged:
                if loginLogic.LoggedEntity == 'ADMIN': g.session.AdminInd = 1
                else: g.session.AdminInd = 0
                
                user = User(UserId=loginLogic.UserId, data_access=g.data_access)
                user.DBFetch(loginLogic.UserId)
                
                g.session.UserId = loginLogic.UserId
                g.session.LoggedInInd = 1
                g.session.LoggedinEntityName = user.Firstname
                g.session.Save()
                    
                return redirect(url_for('welcome_view', sessionGuid=g.session.SessionGuid))
            
            resp = make_response(render_template(form_url, form=form))
            return resp
        except LoginError as login_error:
            g.app_has_errors = True
            flash(login_error.message, "danger")
            resp = make_response(render_template(form_url, form=form))
            return resp

    if g.session.LoggedInInd == 1:
        return redirect(url_for('welcome_view', sessionGuid=g.session.SessionGuid))

    resp = make_response(render_template(form_url, form=form))
    return resp


@app.route("/welcome/<string:sessionGuid>", methods=['GET', 'POST'])
def welcome_view(sessionGuid):
    form = WelcomeForm()
    form_url = 'Profiles/welcome.html'

    if form.RequireLoginInd and g.session.LoggedInInd != 1:
        clear_session_variables()
        return redirect(url_for('home_view'))
    
    if form.AdministratorForm and g.session.AdminInd != 1:
        clear_session_variables()
        return redirect(url_for('home_view'))

    if g.session.SessionGuid != sessionGuid:
        clear_session_variables()
        return redirect(url_for('home_view'))

    userType = 'NORMAL'
    
    if g.session.AdminInd == 1:
        sideMenuItems = _get_Admin_SideMenuItems()
        userType = 'ADMIN'
    else:
        sideMenuItems = _get_Normal_SideMenuItems()

    meetings = get_AdminMeetings()

    resp = make_response(render_template(form_url, form=form, meetings=meetings, userType=userType,
                         sideMenuItems=sideMenuItems, loggedinEntityName=g.session.LoggedinEntityName))
    return resp

@app.route("/profile/<string:sessionGuid>", methods=["GET", "POST"])
def profile_view(sessionGuid):
    form = ProfileForm()
    form_url = 'Profiles/profile.html'

    if form.RequireLoginInd and g.session.LoggedInInd != 1:
        clear_session_variables()
        return redirect(url_for('home_view'))

    if form.AdministratorForm and g.session.AdminInd != 1:
        clear_session_variables()
        return redirect(url_for('home_view'))

    if g.session.SessionGuid != sessionGuid:
        clear_session_variables()
        return redirect(url_for('home_view'))

    if g.session.AdminInd == 1: sideMenuItems = _get_Admin_SideMenuItems()
    else: sideMenuItems = _get_Normal_SideMenuItems()

    if form.validate_on_submit():
        try:
            firstname = form.userFirstname.data
            lastname = form.userLastname.data
            email = form.userEmail.data

            password = form.newPassword.data
            repeatPassword = form.newConfirmPassword.data
            
            if firstname is None or len(firstname) < 1: raise InputError('Make sure that Firstname has a value')
            if lastname is None or len(lastname) < 1: raise InputError('Make sure that Lastname has a value')
            
            user = User(UserId=g.session.UserId, data_access=g.data_access)
            user.DBFetch(g.session.UserId)
            user.Firstname = firstname
            user.Lastname = lastname
            
            if (password is not None and len(password) > 0) or (repeatPassword is not None and len(repeatPassword) > 0):
                if password == repeatPassword:
                    aes = AESCipher(sysConfig.ENCRYPTION_KEY)
                    newPassword = aes.encrypt(password)
                    user.Password = newPassword
                else:
                    raise InputError('Make sure that you leave password fields empty if you are not updating the password, or make sure that they two fields matches.')
            
            user.Save()
            
            session = Session(SessionId=g.session.SessionId, data_access=g.data_access)
            session.DBFetch(g.session.SessionId)
            session.LoggedinEntityName = user.Firstname
            session.Save()
            
            flash("Profile successfully updated", "success")
            resp = make_response(render_template(form_url, form=form, sideMenuItems=sideMenuItems,
                                 sessionGuid=g.session.SessionGuid, loggedinEntityName=user.Firstname))
            return resp
        except InsertError as insert_error:
            g.app_has_errors = True
            flash(insert_error.message, "danger")
            resp = make_response(render_template(form_url, form=form, sideMenuItems=sideMenuItems, sessionGuid=g.session.SessionGuid,loggedinEntityName=g.session.LoggedinEntityName))
            return resp
        except InputError as input_error:
            g.app_has_errors = True
            flash(input_error.message, "danger")
            resp = make_response(render_template(form_url, form=form, sideMenuItems=sideMenuItems, sessionGuid=g.session.SessionGuid,loggedinEntityName=g.session.LoggedinEntityName))
            return resp


    member = User(UserId=g.session.UserId, data_access=g.data_access)
    member.DBFetch(g.session.UserId)

    form.userFirstname.data = member.Firstname
    form.userLastname.data = member.Lastname
    form.userEmail.data = member.Email

    return render_template(form_url, form=form, sideMenuItems=sideMenuItems, sessionGuid=g.session.SessionGuid,loggedinEntityName=g.session.LoggedinEntityName)


@app.route("/pastmeetings/<string:sessionGuid>", methods=["GET", "POST"])
def pastmeetings_view(sessionGuid):
    form = MeetingForm()
    form_url = 'Profiles/Features/pastmeetings.html'

    if form.RequireLoginInd and g.session.LoggedInInd != 1:
        clear_session_variables()
        return redirect(url_for('home_view'))

    if form.AdministratorForm and g.session.AdminInd != 1:
        clear_session_variables()
        return redirect(url_for('home_view'))

    if g.session.SessionGuid != sessionGuid:
        clear_session_variables()
        return redirect(url_for('home_view'))

    if g.session.AdminInd == 1:
        sideMenuItems = _get_Admin_SideMenuItems()
    else:
        sideMenuItems = _get_Normal_SideMenuItems()

    meetings = get_PastMeetings()
    return render_template(form_url, form=form, meetings=meetings, sideMenuItems=sideMenuItems, sessionGuid=g.session.SessionGuid, loggedinEntityName=g.session.LoggedinEntityName)


@app.route("/managemeetings/<string:sessionGuid>", methods=["GET", "POST"])
def managemeetings_view(sessionGuid):
    form = MeetingForm()
    form_url = 'Profiles/Features/Admin/managemeetings.html'

    if form.RequireLoginInd and g.session.LoggedInInd != 1:
        clear_session_variables()
        return redirect(url_for('home_view'))

    if form.AdministratorForm and g.session.AdminInd != 1:
        clear_session_variables()
        return redirect(url_for('home_view'))

    if g.session.SessionGuid != sessionGuid:
        clear_session_variables()
        return redirect(url_for('home_view'))

    if g.session.AdminInd == 1: sideMenuItems = _get_Admin_SideMenuItems()
    else: sideMenuItems = _get_Normal_SideMenuItems()

    meetings = []

    if form.validate_on_submit():
        try:
            meetingTypeId = form.meetingType.raw_data[0]
            meetingOnlineLink = form.meetingOnlineLink.data
            meetingRoom = form.meetingRoom.data
            meetingBuilding = form.meetingBuilding.data
            meetingStreet = form.meetingStreet.data
            meetingTown = form.meetingTown.data
            meetingTitle = form.meetingTitle.data
            meetingStartDate = form.meetingStartDate.data
            meetingEndDate = form.meetingEndDate.data
            
            agm = form.agmInd.data
            boardUser = form.boardUserInd.data
            financeAuditRisk = form.financeAuditRiskInd.data
            projectReviewCommittee = form.projectReviewCommitteeInd.data
            remco = form.remcoInd.data
            
            presentTime = datetime.datetime.now()
            
            if meetingStartDate < presentTime: raise UpdateError('Meeting cannot be in the past.')
            if meetingStartDate > meetingEndDate: raise UpdateError('Meeting cannot end before it starts.')
            
            if meetingOnlineLink is None or meetingOnlineLink == '':
                if (meetingRoom is None or meetingRoom == '') and (meetingBuilding is None or meetingBuilding == '') and (meetingStreet is None or meetingStreet == '') and (meetingTown is None or meetingTown == ''):
                    raise InsertError('Meeting location details is missing')
                
                if meetingTown is None or meetingTown == '':
                    raise InsertError('Meeting town must be provided when there is no online link')
            
            if (meetingRoom is not None and meetingRoom != '') or (meetingBuilding is not None and meetingBuilding != '') or (meetingStreet is not None and meetingStreet != ''):
                if meetingTown is None or meetingTown == '':
                    raise InsertError('Meeting town must be provided if room, building or street is provided')
            
            if not (agm or boardUser or financeAuditRisk or projectReviewCommittee or remco):
                raise CaptureError('Please select at least one Access Group')
            
            location = Location(LocationId=None,
                                OnlineLink=meetingOnlineLink,
                                Room=meetingRoom,
                                Building=meetingBuilding,
                                Street=meetingStreet,
                                Town=meetingTown, 
                                data_access=g.data_access)
            location.Save()
            
            meeting = Meeting(MeetingId=None,
                              MeetingTypeId=meetingTypeId,
                              HostId = g.session.UserId,
                              LocationId = location.LocationId[0],
                              Title=meetingTitle,
                              StartDate=meetingStartDate,
                              EndDate=meetingEndDate,
                              data_access=g.data_access)
            
            meeting.Save()
            
            pythonSQL = PythonSQL()
            
            invited_members_ids = []
            invited_members = []

            if form.agmInd.data: 
                accessGroup = pythonSQL.getAccessGroupByName('AGM', g.data_access)
                meetingInvitation = MeetingInvitation(MeetingId=meeting.MeetingId[0], 
                                                      AccessGroupId=accessGroup.AccessGroupId,
                                                      data_access=g.data_access)
                meetingInvitation.Save()
                
                userAccessGroups = pythonSQL.getUserAccessGroups(accessGroup.AccessGroupId, g.data_access)
                for userAccessGroup in userAccessGroups:
                    if userAccessGroup.UserId not in invited_members_ids:
                        invited_members_ids.append(userAccessGroup.UserId)
                        invited_user = User(UserId=userAccessGroup.UserId, data_access=g.data_access)
                        invited_user.DBFetch(userAccessGroup.UserId)
                        invited_members.append(invited_user)

            if form.boardUserInd.data: 
                accessGroup = pythonSQL.getAccessGroupByName('BOARD USER', g.data_access)
                meetingInvitation = MeetingInvitation(MeetingId=meeting.MeetingId[0], 
                                                      AccessGroupId=accessGroup.AccessGroupId,
                                                      data_access=g.data_access)
                meetingInvitation.Save()
                
                userAccessGroups = pythonSQL.getUserAccessGroups(accessGroup.AccessGroupId, g.data_access)
                for userAccessGroup in userAccessGroups:
                    if userAccessGroup.UserId not in invited_members_ids:
                        invited_members_ids.append(userAccessGroup.UserId)
                        invited_user = User(UserId=userAccessGroup.UserId, data_access=g.data_access)
                        invited_user.DBFetch(userAccessGroup.UserId)
                        invited_members.append(invited_user)

            if form.financeAuditRiskInd.data: 
                accessGroup = pythonSQL.getAccessGroupByName('FINANCE AUDIT RISK', g.data_access)
                meetingInvitation = MeetingInvitation(MeetingId=meeting.MeetingId[0], 
                                                      AccessGroupId=accessGroup.AccessGroupId,
                                                      data_access=g.data_access)
                meetingInvitation.Save()
                
                userAccessGroups = pythonSQL.getUserAccessGroups(accessGroup.AccessGroupId, g.data_access)
                for userAccessGroup in userAccessGroups:
                    if userAccessGroup.UserId not in invited_members_ids:
                        invited_members_ids.append(userAccessGroup.UserId)
                        invited_user = User(UserId=userAccessGroup.UserId, data_access=g.data_access)
                        invited_user.DBFetch(userAccessGroup.UserId)
                        invited_members.append(invited_user)

            if form.projectReviewCommitteeInd.data: 
                accessGroup = pythonSQL.getAccessGroupByName('PROJECT REVIEW COMMITTEE', g.data_access)
                meetingInvitation = MeetingInvitation(MeetingId=meeting.MeetingId[0], 
                                                      AccessGroupId=accessGroup.AccessGroupId,
                                                      data_access=g.data_access)
                meetingInvitation.Save()
                
                userAccessGroups = pythonSQL.getUserAccessGroups(accessGroup.AccessGroupId, g.data_access)
                for userAccessGroup in userAccessGroups:
                    if userAccessGroup.UserId not in invited_members_ids:
                        invited_members_ids.append(userAccessGroup.UserId)
                        invited_user = User(UserId=userAccessGroup.UserId, data_access=g.data_access)
                        invited_user.DBFetch(userAccessGroup.UserId)
                        invited_members.append(invited_user)

            if form.remcoInd.data:
                accessGroup = pythonSQL.getAccessGroupByName('REMCO', g.data_access)
                meetingInvitation = MeetingInvitation(MeetingId=meeting.MeetingId[0], 
                                                      AccessGroupId=accessGroup.AccessGroupId,
                                                      data_access=g.data_access)
                meetingInvitation.Save()
                
                userAccessGroups = pythonSQL.getUserAccessGroups(accessGroup.AccessGroupId, g.data_access)
                for userAccessGroup in userAccessGroups:
                    if userAccessGroup.UserId not in invited_members_ids:
                        invited_members_ids.append(userAccessGroup.UserId)
                        invited_user = User(UserId=userAccessGroup.UserId, data_access=g.data_access)
                        invited_user.DBFetch(userAccessGroup.UserId)
                        invited_members.append(invited_user)

            meetings = get_AdminMeetings()
            
            email_meeting_invite(invited_members, meeting)
            
            flash("Meeting successfully saved", "success")
            resp = make_response(redirect(url_for('managemeetings_view', meetings=meetings, sideMenuItems=sideMenuItems, sessionGuid=g.session.SessionGuid,loggedinEntityName=g.session.LoggedinEntityName)))
            return resp
        except InsertError as insert_error:
            g.app_has_errors = True
            flash(insert_error.message, "danger")
            resp = make_response(render_template(form_url, form=form, meetings=meetings, sideMenuItems=sideMenuItems, sessionGuid=g.session.SessionGuid,loggedinEntityName=g.session.LoggedinEntityName))
            return resp
        except UpdateError as update_error:
            g.app_has_errors = True
            flash(update_error.message, "danger")
            resp = make_response(render_template(form_url, form=form, meetings=meetings, sideMenuItems=sideMenuItems, sessionGuid=g.session.SessionGuid,loggedinEntityName=g.session.LoggedinEntityName))
            return resp
        except CaptureError as capture_error:
            g.app_has_errors = True
            flash(capture_error.message, "danger")
            resp = make_response(render_template(form_url, form=form, meetings=meetings, sideMenuItems=sideMenuItems, sessionGuid=g.session.SessionGuid,loggedinEntityName=g.session.LoggedinEntityName))
            return resp
        
    meetings = get_AdminMeetings()
    return render_template(form_url, form=form, meetings=meetings, sideMenuItems=sideMenuItems, sessionGuid=g.session.SessionGuid,loggedinEntityName=g.session.LoggedinEntityName)

def get_AdminMeetings():
    storedProc = StoredProcs() 
    result = storedProc.getInvitedActiveMeetings(g.session.UserId, g.data_access)
    
    meetings = []
    countMeetings = 0
    
    for systemMeeting in result:
        meeting = Meeting(MeetingId=systemMeeting.MeetingId, data_access=g.data_access)
        meeting.DBFetch(systemMeeting.MeetingId)
        
        meetingType = MeetingType(MeetingTypeId=meeting.MeetingTypeId, data_access=g.data_access)
        meetingType.DBFetch(meeting.MeetingTypeId)
        
        host = User(UserId=meeting.HostId, data_access=g.data_access)
        host.DBFetch(meeting.HostId)
        
        location = Location(LocationId=meeting.LocationId, data_access=g.data_access)
        location.DBFetch(meeting.LocationId)
        
        editLink = str(g.domain_name) + str(url_for('editmeeting_view', sessionGuid=g.session.SessionGuid, meetingId=meeting.MeetingId))[1:]  
        deleteLink = str(g.domain_name) + str(url_for('deletemeeting_view', sessionGuid=g.session.SessionGuid, meetingId=meeting.MeetingId))[1:] 
        viewLink = str(g.domain_name) + str(url_for('viewmeeting_view', sessionGuid=g.session.SessionGuid, meetingId=meeting.MeetingId))[1:] 
        
        meetings.append({"meetingType": meetingType.Name,
                         "meetingHost": host.Firstname + ' ' + host.Lastname,
                         "meetingOnlineLink": location.OnlineLink,
                         "meetingRoom": location.Room,
                         "meetingBuilding": location.Building,
                         "meetingStreet": location.Street,
                         "meetingTown": location.Town,
                         "meetingTitle": meeting.Title,
                         "meetingStartDate": meeting.StartDate,
                         "meetingEndDate": meeting.EndDate,
                         "editLink": editLink,
                         "deleteLink": deleteLink,
                         "viewLink": viewLink
                    })
    
    return meetings

def get_PastMeetings():
    storedProc = StoredProcs() 
    result = storedProc.getInvitedPastMeetings(g.session.UserId, g.data_access)
    
    meetings = []
    countMeetings = 0
    
    for systemMeeting in result:
        meeting = Meeting(MeetingId=systemMeeting.MeetingId, data_access=g.data_access)
        meeting.DBFetch(systemMeeting.MeetingId)
        
        meetingType = MeetingType(MeetingTypeId=meeting.MeetingTypeId, data_access=g.data_access)
        meetingType.DBFetch(meeting.MeetingTypeId)
        
        host = User(UserId=meeting.HostId, data_access=g.data_access)
        host.DBFetch(meeting.HostId)
        
        location = Location(LocationId=meeting.LocationId, data_access=g.data_access)
        location.DBFetch(meeting.LocationId)
        
        editLink = str(g.domain_name) + str(url_for('editmeeting_view', sessionGuid=g.session.SessionGuid, meetingId=meeting.MeetingId))[1:]  
        deleteLink = str(g.domain_name) + str(url_for('deletemeeting_view', sessionGuid=g.session.SessionGuid, meetingId=meeting.MeetingId))[1:] 
        viewLink = str(g.domain_name) + str(url_for('viewmeeting_view', sessionGuid=g.session.SessionGuid, meetingId=meeting.MeetingId))[1:] 
        
        meetings.append({"meetingType": meetingType.Name,
                         "meetingHost": host.Firstname + ' ' + host.Lastname,
                         "meetingOnlineLink": location.OnlineLink,
                         "meetingRoom": location.Room,
                         "meetingBuilding": location.Building,
                         "meetingStreet": location.Street,
                         "meetingTown": location.Town,
                         "meetingTitle": meeting.Title,
                         "meetingStartDate": meeting.StartDate,
                         "meetingEndDate": meeting.EndDate,
                         "editLink": editLink,
                         "deleteLink": deleteLink,
                         "viewLink": viewLink
                    })
    
    return meetings

@app.route("/meeting/delete/<string:sessionGuid>/<int:meetingId>", methods=['GET', 'POST'])
def deletemeeting_view(sessionGuid, meetingId):
    form = MeetingForm()
    form_url = 'Profiles/Features/Admin/managemeetings.html'

    if form.RequireLoginInd and g.session.LoggedInInd != 1:
        clear_session_variables()
        return redirect(url_for('home_view'))

    if form.AdministratorForm and g.session.AdminInd != 1:
        clear_session_variables()
        return redirect(url_for('home_view'))

    if g.session.SessionGuid != sessionGuid:
        clear_session_variables()
        return redirect(url_for('home_view'))

    if g.session.AdminInd == 1: sideMenuItems = _get_Admin_SideMenuItems()
    else: sideMenuItems = _get_Normal_SideMenuItems()
    
    try:
        systemUserRoles = Lists()
        meetingInvitations = systemUserRoles.meetingInvitations(meetingId)

        for meetingInvitation in meetingInvitations:
            MI = MeetingInvitation(MeetingInvitationId=meetingInvitation.MeetingInvitationId, data_access=g.data_access)
            MI.DBFetch(meetingInvitation.MeetingInvitationId)
            MI.Delete()

        meeting = Meeting(MeetingId=meetingId, data_access=g.data_access)
        meeting.DBFetch(meetingId)
        meeting.Delete()
        
        location = Location(LocationId=meeting.LocationId, data_access=g.data_access)
        location.DBFetch(meeting.LocationId)
        location.Delete()
        
    except DeleteError as delete_error:
        g.app_has_errors = True
        flash(delete_error.message, "danger")
        resp = make_response(render_template(form_url, form=form, sideMenuItems=sideMenuItems, sessionGuid=g.session.SessionGuid,loggedinEntityName=g.session.LoggedinEntityName))
        return resp
    
    flash("Meeting successfully deleted", "success")
    resp = make_response(redirect(url_for('managemeetings_view', sessionGuid=g.session.SessionGuid, sideMenuItems=sideMenuItems,loggedinEntityName=g.session.LoggedinEntityName)))
    return resp

@app.route("/meeting/edit/<string:sessionGuid>/<int:meetingId>", methods=['GET', 'POST'])
def editmeeting_view(sessionGuid, meetingId):
    form = MeetingForm()
    formAddDocument = FileForm()
    form_url = 'Profiles/Features/Admin/editmeeting.html'

    if form.RequireLoginInd and g.session.LoggedInInd != 1:
        clear_session_variables()
        return redirect(url_for('home_view'))

    if form.AdministratorForm and g.session.AdminInd != 1:
        clear_session_variables()
        return redirect(url_for('home_view'))

    if g.session.SessionGuid != sessionGuid:
        clear_session_variables()
        return redirect(url_for('home_view'))

    if g.session.AdminInd == 1: sideMenuItems = _get_Admin_SideMenuItems()
    else:
        sideMenuItems = _get_Normal_SideMenuItems()
            
    pythonSQL = PythonSQL()

    if form.meetingAdd.data and form.validate_on_submit():
        try:
            meetingTypeId = form.meetingType.raw_data[0]
            meetingOnlineLink = form.meetingOnlineLink.data
            meetingRoom = form.meetingRoom.data
            meetingBuilding = form.meetingBuilding.data
            meetingStreet = form.meetingStreet.data
            meetingTown = form.meetingTown.data
            meetingTitle = form.meetingTitle.data
            meetingStartDate = form.meetingStartDate.data
            meetingEndDate = form.meetingEndDate.data

            agm = form.agmInd.data
            if agm:
                agmInd = 1
            else:
                agmInd = 0

            boardUser = form.boardUserInd.data
            if boardUser:
                boardUserInd = 1
            else:
                boardUserInd = 0

            financeAuditRisk = form.financeAuditRiskInd.data
            if financeAuditRisk:
                financeAuditRiskInd = 1
            else:
                financeAuditRiskInd = 0

            projectReviewCommittee = form.projectReviewCommitteeInd.data
            if projectReviewCommittee:
                projectReviewCommitteeInd = 1
            else:
                projectReviewCommitteeInd = 0

            remco = form.remcoInd.data
            if remco:
                remcoInd = 1
            else:
                remcoInd = 0
            
            presentTime = datetime.datetime.now()
            
            if meetingStartDate < presentTime: raise UpdateError('Meeting cannot be in the past.')
            if meetingStartDate > meetingEndDate: raise UpdateError('Meeting cannot end before it starts.')
            
            if meetingOnlineLink is None or meetingOnlineLink == '':
                if (meetingRoom is None or meetingRoom == '') and (meetingBuilding is None or meetingBuilding == '') and (meetingStreet is None or meetingStreet == '') and (meetingTown is None or meetingTown == ''):
                    raise InsertError('Meeting location details is missing')
                
                if meetingTown is None or meetingTown == '':
                    raise InsertError('Meeting town must be provided when there is no online link')
            
            if (meetingRoom is not None and meetingRoom != '') or (meetingBuilding is not None and meetingBuilding != '') or (meetingStreet is not None and meetingStreet != ''):
                if meetingTown is None or meetingTown == '':
                    raise InsertError('Meeting town must be provided if room, building or street is provided')
            
            if not (agm or boardUser or financeAuditRisk or projectReviewCommittee or remco):
                raise CaptureError('Please select at least one Access Group')
            
            meeting = Meeting(MeetingId=meetingId, data_access=g.data_access)
            meeting.DBFetch(meetingId)
            meeting.MeetingTypeId = meetingTypeId
            meeting.Title = meetingTitle
            meeting.StartDate = meetingStartDate
            meeting.EndDate = meetingEndDate
            meeting.Save()
            
            location = Location(LocationId=meeting.LocationId, data_access=g.data_access)
            location.DBFetch(meeting.LocationId)
            location.OnlineLink = meetingOnlineLink
            location.Room = meetingRoom
            location.Building = meetingBuilding
            location.Street = meetingStreet
            location.Town = meetingTown
            location.Save()

            accessGroup = pythonSQL.getAccessGroupByName('AGM', g.data_access)
            CaptureMeetingInvitationCheckBoxField(agm, meetingId, accessGroup.AccessGroupId)

            accessGroup = pythonSQL.getAccessGroupByName('BOARD USER', g.data_access)
            CaptureMeetingInvitationCheckBoxField(boardUser, meetingId, accessGroup.AccessGroupId)

            accessGroup = pythonSQL.getAccessGroupByName('FINANCE AUDIT RISK', g.data_access)
            CaptureMeetingInvitationCheckBoxField(financeAuditRisk, meetingId, accessGroup.AccessGroupId)

            accessGroup = pythonSQL.getAccessGroupByName('PROJECT REVIEW COMMITTEE', g.data_access)
            CaptureMeetingInvitationCheckBoxField(projectReviewCommittee, meetingId, accessGroup.AccessGroupId)

            accessGroup = pythonSQL.getAccessGroupByName('REMCO', g.data_access)
            CaptureMeetingInvitationCheckBoxField(remco, meetingId, accessGroup.AccessGroupId)

            flash("Meeting successfully saved", "success")
            
            files = get_PermittedFiles(g.session.UserId, meetingId)
            
            resp = make_response(redirect(url_for('editmeeting_view', files=files, sideMenuItems=sideMenuItems, sessionGuid=g.session.SessionGuid, meetingId=meetingId,loggedinEntityName=g.session.LoggedinEntityName)))
            return resp
        except InsertError as insert_error:
            g.app_has_errors = True
            flash(insert_error.message, "danger")
            
            files = get_PermittedFiles(g.session.UserId, meetingId)
            
            resp = make_response(render_template(form_url, files=files, form=form, formAddDocument=formAddDocument, sideMenuItems=sideMenuItems, sessionGuid=g.session.SessionGuid, meetingId=meetingId,loggedinEntityName=g.session.LoggedinEntityName))
            return resp
        except UpdateError as update_error:
            g.app_has_errors = True
            flash(update_error.message, "danger")
            
            files = get_PermittedFiles(g.session.UserId, meetingId)
            
            resp = make_response(render_template(form_url, files=files, form=form, formAddDocument=formAddDocument, sideMenuItems=sideMenuItems, sessionGuid=g.session.SessionGuid, meetingId=meetingId,loggedinEntityName=g.session.LoggedinEntityName))
            return resp
        except CaptureError as capture_error:
            g.app_has_errors = True
            flash(capture_error.message, "danger")
            
            files = get_PermittedFiles(g.session.UserId, meetingId)
            
            resp = make_response(render_template(form_url, files=files, form=form, formAddDocument=formAddDocument, sideMenuItems=sideMenuItems, sessionGuid=g.session.SessionGuid, meetingId=meetingId,loggedinEntityName=g.session.LoggedinEntityName))
            return resp
    elif formAddDocument.fileSave.data and formAddDocument.validate_on_submit():
        try:
            agm = formAddDocument.agmInd.data
            boardUser = formAddDocument.boardUserInd.data
            financeAuditRisk = formAddDocument.financeAuditRiskInd.data
            projectReviewCommittee = formAddDocument.projectReviewCommitteeInd.data
            remco = formAddDocument.remcoInd.data

            if 'fileContent' not in request.files:
                raise FileMissingError('File is not attached')

            uploadedFile = request.files['fileContent']
            file_extension = get_file_extension(uploadedFile.filename)

            if not allowed_file(uploadedFile.filename):
                raise FileMissingError('File type is not allowed')
            elif uploadedFile.content_length > app.config['MAX_CONTENT_LENGTH']:
                raise FileSizeError('File is larger than 16MB')

            meetingFile = File(Name=formAddDocument.fileName.data, Path=str(uuid.uuid4()) + '.' + file_extension, data_access=g.data_access)
        
            if meetingFile.Name is None or meetingFile.Name == '':
                raise CaptureError('File name is not captured')
            
            if not (agm or boardUser or financeAuditRisk or projectReviewCommittee or remco):
                raise CaptureError('Please select at least one Access Group')
            
            meetingFile.Save()
            mf = MeetingFile(MeetingId=meetingId, FileId=meetingFile.FileId[0], data_access=g.data_access)
            mf.Save()
            
            pythonSQL = PythonSQL()

            if formAddDocument.agmInd.data: 
                accessGroup = pythonSQL.getAccessGroupByName('AGM', g.data_access)
                fileAccess = FileAccess(FileId=meetingFile.FileId[0], 
                                        AccessGroupId=accessGroup.AccessGroupId,
                                        data_access=g.data_access)
                fileAccess.Save()

            if formAddDocument.boardUserInd.data: 
                accessGroup = pythonSQL.getAccessGroupByName('BOARD USER', g.data_access)
                fileAccess = FileAccess(FileId=meetingFile.FileId[0], 
                                        AccessGroupId=accessGroup.AccessGroupId,
                                        data_access=g.data_access)
                fileAccess.Save()

            if formAddDocument.financeAuditRiskInd.data: 
                accessGroup = pythonSQL.getAccessGroupByName('FINANCE AUDIT RISK', g.data_access)
                fileAccess = FileAccess(FileId=meetingFile.FileId[0], 
                                        AccessGroupId=accessGroup.AccessGroupId,
                                        data_access=g.data_access)
                fileAccess.Save()

            if formAddDocument.projectReviewCommitteeInd.data: 
                accessGroup = pythonSQL.getAccessGroupByName('PROJECT REVIEW COMMITTEE', g.data_access)
                fileAccess = FileAccess(FileId=meetingFile.FileId[0], 
                                        AccessGroupId=accessGroup.AccessGroupId,
                                        data_access=g.data_access)
                fileAccess.Save()

            if formAddDocument.remcoInd.data:
                accessGroup = pythonSQL.getAccessGroupByName('REMCO', g.data_access)
                fileAccess = FileAccess(FileId=meetingFile.FileId[0], 
                                        AccessGroupId=accessGroup.AccessGroupId,
                                        data_access=g.data_access)
                fileAccess.Save()

            uploadedFile.save(app.config['UPLOAD_FOLDER'] + meetingFile.Path)
            
            files = get_PermittedFiles(g.session.UserId, meetingId)
            
            flash("File uploaded successfully.", "success")
            return redirect(url_for('editmeeting_view', files=files, form=form, formAddDocument=formAddDocument, sideMenuItems=sideMenuItems, sessionGuid=g.session.SessionGuid, meetingId=meetingId,loggedinEntityName=g.session.LoggedinEntityName))
            #return resp
            #return redirect(url_for('editmeeting_view'))
        except InsertError as insert_error:
            g.app_has_errors = True
            flash(insert_error.message, "danger")
            
            files = get_PermittedFiles(g.session.UserId, meetingId)
            
            resp = make_response(render_template(form_url, files=files, form=form, formAddDocument=formAddDocument, sideMenuItems=sideMenuItems, sessionGuid=g.session.SessionGuid, meetingId=meetingId,loggedinEntityName=g.session.LoggedinEntityName))
            return resp
        except UpdateError as update_error:
            g.app_has_errors = True
            flash(update_error.message, "danger")
            
            files = get_PermittedFiles(g.session.UserId, meetingId)
            
            resp = make_response(render_template(form_url, files=files, form=form, formAddDocument=formAddDocument, sideMenuItems=sideMenuItems, sessionGuid=g.session.SessionGuid, meetingId=meetingId,loggedinEntityName=g.session.LoggedinEntityName))
            return resp
        except FileMissingError as file_missing_error:
            g.app_has_errors = True
            flash(file_missing_error.message, "danger")
            
            files = get_PermittedFiles(g.session.UserId, meetingId)
            
            resp = make_response(render_template(form_url, files=files, form=form, formAddDocument=formAddDocument, sideMenuItems=sideMenuItems, sessionGuid=g.session.SessionGuid, meetingId=meetingId,loggedinEntityName=g.session.LoggedinEntityName))
            return resp
        except FileSizeError as file_size_error:
            g.app_has_errors = True
            flash(file_size_error.message, "danger")
            
            files = get_PermittedFiles(g.session.UserId, meetingId)
            
            resp = make_response(render_template(form_url, files=files, form=form, formAddDocument=formAddDocument, sideMenuItems=sideMenuItems, sessionGuid=g.session.SessionGuid, meetingId=meetingId,loggedinEntityName=g.session.LoggedinEntityName))
            return resp

    meeting = Meeting(MeetingId=meetingId, data_access=g.data_access)
    meeting.DBFetch(meetingId)
    
    location = Location(LocationId=meeting.LocationId, data_access=g.data_access)
    location.DBFetch(meeting.LocationId)
            
    form.meetingType.process_data(meeting.MeetingTypeId)
    form.meetingOnlineLink.data = location.OnlineLink
    form.meetingRoom.data = location.Room
    form.meetingBuilding.data = location.Building
    form.meetingStreet.data = location.Street
    form.meetingTown.data = location.Town
    form.meetingTitle.data = meeting.Title
    form.meetingStartDate.data = meeting.StartDate
    form.meetingEndDate.data = meeting.EndDate

    accessGroup = pythonSQL.getAccessGroupByName('AGM', g.data_access)
    meetingInvitation = pythonSQL.getMeetingInvitation(meetingId, accessGroup.AccessGroupId, g.data_access)
    form.agmInd.data = meetingInvitation != None

    accessGroup = pythonSQL.getAccessGroupByName('BOARD USER', g.data_access)
    meetingInvitation = pythonSQL.getMeetingInvitation(meetingId, accessGroup.AccessGroupId, g.data_access)
    form.boardUserInd.data = meetingInvitation != None

    accessGroup = pythonSQL.getAccessGroupByName('FINANCE AUDIT RISK', g.data_access)
    meetingInvitation = pythonSQL.getMeetingInvitation(meetingId, accessGroup.AccessGroupId, g.data_access)
    form.financeAuditRiskInd.data = meetingInvitation != None

    accessGroup = pythonSQL.getAccessGroupByName('PROJECT REVIEW COMMITTEE', g.data_access)
    meetingInvitation = pythonSQL.getMeetingInvitation(meetingId, accessGroup.AccessGroupId, g.data_access)
    form.projectReviewCommitteeInd.data = meetingInvitation != None

    accessGroup = pythonSQL.getAccessGroupByName('REMCO', g.data_access)
    meetingInvitation = pythonSQL.getMeetingInvitation(meetingId, accessGroup.AccessGroupId, g.data_access)
    form.remcoInd.data = meetingInvitation != None
            
    files = get_PermittedFiles(g.session.UserId, meetingId)        
            
    return render_template(form_url, files=files, form=form, formAddDocument=formAddDocument, sideMenuItems=sideMenuItems, sessionGuid=g.session.SessionGuid, meetingId=meetingId,loggedinEntityName=g.session.LoggedinEntityName)

def email_meeting_invite(members, meeting):
    for member in members:
        subject = "Meeting Invitation"
        sender = "emeeting@jtgd-trust.co.za"
        recipients = [member.Email]
        body = "Good day,\n\nYou are invited to a meeting as scheduled:\n\n"
        body = body + "Title: " + meeting.Title
        body = body + "\n"
        body = body + "Date: " + str(meeting.StartDate)
        body = body + "\n\n"
        body = body + "Please login on eBoardMeeting to access the meeting. Login at "
        body = body + str(g.domain_name) 
        body = body + "\n\n"
        body = body + "Regards"
        SendRegistrationEmail(subject=subject, sender=sender, recipients=recipients, body=body)



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def get_file_extension(filename):
    return filename.rsplit('.', 1)[1]

def get_PermittedFiles(userId, meetingId):
    storedProc = StoredProcs()

    permittedFilesData = storedProc.getPermittedFiles(userId, meetingId, g.data_access)

    permittedFiles = []
    
    for permittedFile in permittedFilesData:
        deleteLink = str(g.domain_name) + str(url_for('deletefile_view', sessionGuid=g.session.SessionGuid, fileId=permittedFile[0], meetingId=meetingId))[1:] 
        viewLink = str(g.domain_name) + str(url_for('viewfile_view', sessionGuid=g.session.SessionGuid, fileId=permittedFile[0]))[1:] 
        
        permittedFiles.append({
            "fileName":permittedFile[1],
            "viewLink":viewLink,
            "deleteLink": deleteLink
        })
        
    return permittedFiles     

@app.route("/file/view/<string:sessionGuid>/<int:fileId>", methods=['GET', 'POST'])
def viewfile_view(sessionGuid, fileId):
    # https://www.w3docs.com/tools/code-editor/1087
    form = FileForm()
    form_url = 'Profiles/Features/viewfile.html'

    if form.RequireLoginInd and g.session.LoggedInInd != 1:
        clear_session_variables()
        return redirect(url_for('home_view'))

    if form.AdministratorForm and g.session.AdminInd != 1:
        clear_session_variables()
        return redirect(url_for('home_view'))

    if g.session.SessionGuid != sessionGuid:
        clear_session_variables()
        return redirect(url_for('home_view'))
    
    if g.session.AdminInd == 1: sideMenuItems = _get_Admin_SideMenuItems()
    else: sideMenuItems = _get_Normal_SideMenuItems()
    
    file = File(FileId=fileId, data_access=g.data_access)
    file.DBFetch(fileId)
    
    filePath = "/" + app.config['UPLOAD_FOLDER'] + file.Path
    fileName = file.Name
   
    return render_template(form_url, filePath=filePath, fileName=fileName, sideMenuItems=sideMenuItems, sessionGuid=g.session.SessionGuid, fileId=fileId,loggedinEntityName=g.session.LoggedinEntityName)


@app.route("/file/delete/<string:sessionGuid>/<int:fileId>/<int:meetingId>", methods=['GET', 'POST'])
def deletefile_view(sessionGuid, fileId, meetingId):
    form = HomeForm()

    if form.RequireLoginInd and g.session.LoggedInInd != 1:
        clear_session_variables()
        return redirect(url_for('home_view'))

    if form.AdministratorForm and g.session.AdminInd != 1:
        clear_session_variables()
        return redirect(url_for('home_view'))

    if g.session.SessionGuid != sessionGuid:
        clear_session_variables()
        return redirect(url_for('home_view'))
    
    if g.session.AdminInd == 1: sideMenuItems = _get_Admin_SideMenuItems()
    else: sideMenuItems = _get_Normal_SideMenuItems()

    try:
        systemUserRoles = Lists()
        fileAccess = systemUserRoles.fileAccess(fileId)
        
        for uniqueFileAccess in fileAccess:
            FA = FileAccess(FileAccessId=uniqueFileAccess.FileAccessId, data_access=g.data_access)
            FA.DBFetch(uniqueFileAccess.FileAccessId)
            FA.Delete()
            
        meetingFile = systemUserRoles.meetingFile(fileId)
        
        for uniqueMeetingFile in meetingFile:
            MF = MeetingFile(MeetingFileId=uniqueMeetingFile.MeetingFileId, data_access=g.data_access)
            MF.DBFetch(uniqueMeetingFile.MeetingFileId)
            MF.Delete()
            
        file = File(FileId=fileId, data_access=g.data_access)
        file.DBFetch(fileId)
        file.Delete()

        flash("File deleted successfully.", "success")
            
        files = get_PermittedFiles(g.session.UserId, meetingId)
        
        resp = make_response(redirect(url_for('editmeeting_view', files=files, sideMenuItems=sideMenuItems, sessionGuid=g.session.SessionGuid, meetingId=meetingId,loggedinEntityName=g.session.LoggedinEntityName)))
        return resp
    except DeleteError as delete_error:
        g.app_has_errors = True
        flash(delete_error.message, "danger")
        resp = make_response(redirect(url_for('managemeetings_view', sessionGuid=sessionGuid,loggedinEntityName=g.session.LoggedinEntityName)))
        return resp
    except FetchError as fetch_error:
        g.app_has_errors = True
        flash(fetch_error.message, "danger")
        resp = make_response(redirect(url_for('managemeetings_view', sessionGuid=sessionGuid,loggedinEntityName=g.session.LoggedinEntityName)))
        return resp

@app.route("/meeting/view/<string:sessionGuid>/<int:meetingId>", methods=['GET', 'POST'])
def viewmeeting_view(sessionGuid, meetingId):
    form = MeetingForm()
    formAddDocument = FileForm()
    form_url = 'Profiles/Features/viewmeeting.html'

    if form.RequireLoginInd and g.session.LoggedInInd != 1:
        clear_session_variables()
        return redirect(url_for('home_view'))

    if form.AdministratorForm and g.session.AdminInd != 1:
        clear_session_variables()
        return redirect(url_for('home_view'))

    if g.session.SessionGuid != sessionGuid:
        clear_session_variables()
        return redirect(url_for('home_view'))

    userType = 'NORMAL'
    
    if g.session.AdminInd == 1:
        sideMenuItems = _get_Admin_SideMenuItems()
        userType = 'ADMIN'
    else:
        sideMenuItems = _get_Normal_SideMenuItems()
    
    meeting = Meeting(MeetingId=meetingId, data_access=g.data_access)
    meeting.DBFetch(meetingId)
    
    location = Location(LocationId=meeting.LocationId, data_access=g.data_access)
    location.DBFetch(meeting.LocationId)
            
    form.meetingType.process_data(meeting.MeetingTypeId)
    form.meetingOnlineLink.data = location.OnlineLink
    form.meetingRoom.data = location.Room
    form.meetingBuilding.data = location.Building
    form.meetingStreet.data = location.Street
    form.meetingTown.data = location.Town
    form.meetingTitle.data = meeting.Title
    form.meetingStartDate.data = meeting.StartDate
    form.meetingEndDate.data = meeting.EndDate
            
    files = get_PermittedFiles(g.session.UserId, meetingId)     
    
    return render_template(form_url, files=files, userType=userType, form=form, formAddDocument=formAddDocument, sideMenuItems=sideMenuItems, sessionGuid=g.session.SessionGuid, meetingId=meetingId,loggedinEntityName=g.session.LoggedinEntityName)

@app.route("/manageusers/<string:sessionGuid>", methods=["GET", "POST"])
def manageusers_view(sessionGuid):
    form = UserForm()
    form_url = 'Profiles/Features/Admin/manageusers.html'

    if form.RequireLoginInd and g.session.LoggedInInd != 1:
        clear_session_variables()
        return redirect(url_for('home_view'))

    if form.AdministratorForm and g.session.AdminInd != 1:
        clear_session_variables()
        return redirect(url_for('home_view'))

    if g.session.SessionGuid != sessionGuid:
        clear_session_variables()
        return redirect(url_for('home_view'))

    if g.session.AdminInd == 1: sideMenuItems = _get_Admin_SideMenuItems()
    else: sideMenuItems = _get_Normal_SideMenuItems()

    users = get_Users()
            
    pythonSQL = PythonSQL()
    
    if form.validate_on_submit():
        try:
            firstName = form.userFirstname.data
            lastName = form.userLastname.data
            email = form.userEmail.data

            agm = form.agmInd.data
            if agm:
                agmInd = 1
            else:
                agmInd = 0

            boardUser = form.boardUserInd.data
            if boardUser:
                boardUserInd = 1
            else:
                boardUserInd = 0

            financeAuditRisk = form.financeAuditRiskInd.data
            if financeAuditRisk:
                financeAuditRiskInd = 1
            else:
                financeAuditRiskInd = 0

            projectReviewCommittee = form.projectReviewCommitteeInd.data
            if projectReviewCommittee:
                projectReviewCommitteeInd = 1
            else:
                projectReviewCommitteeInd = 0

            remco = form.remcoInd.data
            if remco:
                remcoInd = 1
            else:
                remcoInd = 0
            
            aes = AESCipher(sysConfig.ENCRYPTION_KEY)
            defaultPassword = 'M33t1n9.syst3m'

            member = User(Firstname=firstName,
                          Lastname=lastName,
                          Email=email,
                          Password=aes.encrypt(defaultPassword),
                          RegistrationDate=datetime.datetime.now(),
                          LastAccessDate=datetime.datetime.now(),
                          UniqueLogins=0,
                          PasswordRecovery=str(uuid.uuid4()),
                          data_access=g.data_access)
            
            userId = g.session.MemberId
            
            if g.session.MemberId is not None:
                member = User(UserId=userId, data_access=g.data_access)
                member.DBFetch(g.session.MemberId)
                member.Firstname = firstName
                member.LastName = lastName
                member.Save()
            else:
                member.Save()
                userId = member.UserId[0]

                subject = "New Account!"
                sender = "emeeting@jtgd-trust.co.za"
                recipients = [member.Email]
                body = "Good day,\n\nA new account has been created for you on eBoardMeeting. User the default password provided below:\n\n"
                body = body + "Default Password: " + defaultPassword
                body = body + "\n\n"
                body = body + "Please login and change your password under your profile. eBoardMeeting can be access at "
                body = body + str(g.domain_name) 
                body = body + "\n\n"
                body = body + "Regards"
                SendRegistrationEmail(subject=subject, sender=sender, recipients=recipients, body=body)


            g.session.MemberId = None
            g.session.Save()
            
            if not (agm or boardUser or financeAuditRisk or projectReviewCommittee or remco):
                raise CaptureError('Please select at least one Access Group')

            accessGroup = pythonSQL.getAccessGroupByName('AGM', g.data_access)
            CaptureUserAccessGroupCheckBoxField(agm, userId, accessGroup.AccessGroupId)

            accessGroup = pythonSQL.getAccessGroupByName('BOARD USER', g.data_access)
            CaptureUserAccessGroupCheckBoxField(boardUser, userId, accessGroup.AccessGroupId)

            accessGroup = pythonSQL.getAccessGroupByName('FINANCE AUDIT RISK', g.data_access)
            CaptureUserAccessGroupCheckBoxField(financeAuditRisk, userId, accessGroup.AccessGroupId)

            accessGroup = pythonSQL.getAccessGroupByName('PROJECT REVIEW COMMITTEE', g.data_access)
            CaptureUserAccessGroupCheckBoxField(projectReviewCommittee, userId, accessGroup.AccessGroupId)

            accessGroup = pythonSQL.getAccessGroupByName('REMCO', g.data_access)
            CaptureUserAccessGroupCheckBoxField(remco, userId, accessGroup.AccessGroupId)

            flash("User successfully saved", "success")
            resp = make_response(redirect(url_for('manageusers_view', sessionGuid=g.session.SessionGuid,loggedinEntityName=g.session.LoggedinEntityName)))
            return resp
        except InsertError as insert_error:
            g.app_has_errors = True
            flash(insert_error.message, "danger")
            resp = make_response(render_template(form_url, form=form, users=users, sideMenuItems=sideMenuItems, sessionGuid=g.session.SessionGuid,loggedinEntityName=g.session.LoggedinEntityName))
            return resp
        except UpdateError as update_error:
            g.app_has_errors = True
            flash(update_error.message, "danger")
            resp = make_response(render_template(form_url, form=form, users=users, sideMenuItems=sideMenuItems, sessionGuid=g.session.SessionGuid,loggedinEntityName=g.session.LoggedinEntityName))
            return resp
        except CaptureError as capture_error:
            g.app_has_errors = True
            flash(capture_error.message, "danger")
            resp = make_response(render_template(form_url, form=form, users=users, sideMenuItems=sideMenuItems, sessionGuid=g.session.SessionGuid,loggedinEntityName=g.session.LoggedinEntityName))
            return resp
        
    if g.session.MemberId is not None:
        member = User(UserId=g.session.MemberId, data_access=g.data_access)
        member.DBFetch(g.session.MemberId)

        form.userFirstname.data = member.Firstname
        form.userLastname.data = member.Lastname
        form.userEmail.data = member.Email

        accessGroup = pythonSQL.getAccessGroupByName('AGM', g.data_access)
        userAccessGroup = pythonSQL.getUserAccessGroup(g.session.MemberId, accessGroup.AccessGroupId, g.data_access)
        form.agmInd.data = userAccessGroup != None

        accessGroup = pythonSQL.getAccessGroupByName('BOARD USER', g.data_access)
        userAccessGroup = pythonSQL.getUserAccessGroup(g.session.MemberId, accessGroup.AccessGroupId, g.data_access)
        form.boardUserInd.data = userAccessGroup != None

        accessGroup = pythonSQL.getAccessGroupByName('FINANCE AUDIT RISK', g.data_access)
        userAccessGroup = pythonSQL.getUserAccessGroup(g.session.MemberId, accessGroup.AccessGroupId, g.data_access)
        form.financeAuditRiskInd.data = userAccessGroup != None

        accessGroup = pythonSQL.getAccessGroupByName('PROJECT REVIEW COMMITTEE', g.data_access)
        userAccessGroup = pythonSQL.getUserAccessGroup(g.session.MemberId, accessGroup.AccessGroupId, g.data_access)
        form.projectReviewCommitteeInd.data = userAccessGroup != None

        accessGroup = pythonSQL.getAccessGroupByName('REMCO', g.data_access)
        userAccessGroup = pythonSQL.getUserAccessGroup(g.session.MemberId, accessGroup.AccessGroupId, g.data_access)
        form.remcoInd.data = userAccessGroup != None

    return render_template(form_url, form=form, users=users, sideMenuItems=sideMenuItems, sessionGuid=g.session.SessionGuid,loggedinEntityName=g.session.LoggedinEntityName)

def get_Users():
    systemUserList = Lists() 
    result = systemUserList.Users()
    
    users = []
    countUsers = 0
    
    for systemUser in result:
        user = User(UserId=systemUser.UserId, data_access=g.data_access)
        user.DBFetch(systemUser.UserId)
        
        systemUserRoles = Lists()
        userAccessGroups = systemUserRoles.userAccessGroup(user.UserId)
        
        returnedRoles = []
        
        for uniqueRole in userAccessGroups:
            accessGroup = AccessGroup(AccessGroupId=uniqueRole.AccessGroupId, data_access=g.data_access)
            accessGroup.DBFetch(uniqueRole.AccessGroupId)
            returnedRoles.append(accessGroup.Name)
        
        editLink = str(g.domain_name) + str(url_for('edituser_view', sessionGuid=g.session.SessionGuid, memberId=user.UserId))[1:]  
        deleteLink = str(g.domain_name) + str(url_for('deleteuser_view', sessionGuid=g.session.SessionGuid, memberId=user.UserId))[1:] 
        
        users.append({"firstName": user.Firstname,
                      "lastName": user.Lastname,
                      "email": user.Email,
                      "roles": returnedRoles,
                      "editLink": editLink,
                      "deleteLink": deleteLink
                    })
    
    return users

def CaptureUserAccessGroupCheckBoxField(checkboxField, UserId, AccessGroupId):
    if checkboxField:
        SaveUserAccessGroup(UserId, AccessGroupId)
    else:
        DeleteUserAccessGroup(UserId, AccessGroupId)

def SaveUserAccessGroup(UserId, AccessGroupId):
    pythonSQL = PythonSQL()
    userAccessGroup = pythonSQL.getUserAccessGroup(UserId, AccessGroupId, g.data_access)
    
    if userAccessGroup is None:
        userAccessGroup = UserAccessGroup(UserAccessGroupId=None, UserId=UserId, AccessGroupId=AccessGroupId, data_access=g.data_access)
        userAccessGroup.Save()

def DeleteUserAccessGroup(UserId, AccessGroupId):
    pythonSQL = PythonSQL()
    userAccessGroup = pythonSQL.getUserAccessGroup(UserId, AccessGroupId, g.data_access)
    
    if userAccessGroup is not None:
        userAccessGroup.Delete()

def CaptureMeetingInvitationCheckBoxField(checkboxField, MeetingId, AccessGroupId):
    if checkboxField:
        SaveMeetingInvitation(MeetingId, AccessGroupId)
    else:
        DeleteMeetingInvitation(MeetingId, AccessGroupId)

def SaveMeetingInvitation(MeetingId, AccessGroupId):
    pythonSQL = PythonSQL()
    meetingInvitation = pythonSQL.getMeetingInvitation(MeetingId, AccessGroupId, g.data_access)
    
    if meetingInvitation is None:
        meetingInvitation = MeetingInvitation(MeetingInvitationId=None, MeetingId=MeetingId, AccessGroupId=AccessGroupId, data_access=g.data_access)
        meetingInvitation.Save()

def DeleteMeetingInvitation(MeetingId, AccessGroupId):
    pythonSQL = PythonSQL()
    meetingInvitation = pythonSQL.getMeetingInvitation(MeetingId, AccessGroupId, g.data_access)
    
    if meetingInvitation is not None:
        meetingInvitation.Delete()

@app.route("/user/edit/<string:sessionGuid>/<int:memberId>", methods=['GET', 'POST'])
def edituser_view(sessionGuid, memberId):
    form = UserForm()
    form_url = 'Profiles/Features/Admin/manageusers.html'

    if form.RequireLoginInd and g.session.LoggedInInd != 1:
        clear_session_variables()
        return redirect(url_for('home_view'))

    if form.AdministratorForm and g.session.AdminInd != 1:
        clear_session_variables()
        return redirect(url_for('home_view'))

    if g.session.SessionGuid != sessionGuid:
        clear_session_variables()
        return redirect(url_for('home_view'))

    if g.session.AdminInd == 1:
        sideMenuItems = _get_Admin_SideMenuItems()
    else:
        sideMenuItems = _get_Normal_SideMenuItems()

    g.session.MemberId = memberId
    g.session.Save()

    resp = make_response(redirect(url_for('manageusers_view', sessionGuid=g.session.SessionGuid,loggedinEntityName=g.session.LoggedinEntityName)))
    return resp


@app.route("/user/delete/<string:sessionGuid>/<int:memberId>", methods=['GET', 'POST'])
def deleteuser_view(sessionGuid, memberId): 
    form = HomeForm()

    if form.RequireLoginInd and g.session.LoggedInInd != 1:
        clear_session_variables()
        return redirect(url_for('home_view'))

    if form.AdministratorForm and g.session.AdminInd != 1:
        clear_session_variables()
        return redirect(url_for('home_view'))

    if g.session.SessionGuid != sessionGuid:
        clear_session_variables()
        return redirect(url_for('home_view'))

    try:
        systemUserRoles = Lists()
        userAccessGroups = systemUserRoles.userAccessGroup(memberId)
        
        for uniqueRole in userAccessGroups:
            userAccessGroup = UserAccessGroup(UserAccessGroupId=uniqueRole.UserAccessGroupId, data_access=g.data_access)
            userAccessGroup.DBFetch(uniqueRole.UserAccessGroupId)
            userAccessGroup.Delete()
            
        user = User(UserId=memberId, data_access=g.data_access)
        user.DBFetch(memberId)
        user.Delete()

        flash("User deleted successfully.", "success")
        resp = make_response(redirect(url_for('manageusers_view', sessionGuid=sessionGuid,loggedinEntityName=g.session.LoggedinEntityName)))
        return resp
    except DeleteError as delete_error:
        g.app_has_errors = True
        flash(delete_error.message, "danger")
        resp = make_response(redirect(url_for('manageusers_view', sessionGuid=sessionGuid,loggedinEntityName=g.session.LoggedinEntityName)))
        return resp
    except FetchError as fetch_error:
        g.app_has_errors = True
        flash(fetch_error.message, "danger")
        resp = make_response(redirect(url_for('manageusers_view', sessionGuid=sessionGuid,loggedinEntityName=g.session.LoggedinEntityName)))
        return resp

@app.route("/recoverpassword", methods=['GET', 'POST'])
def recoverpassword_view():
    form = RecoverPasswordForm()

    if form.validate_on_submit():
        try:
            recoverPasswordEmailAddress = form.username.data

            recoverPassordLogic = RecoverPasswordLogic(recoverPasswordEmailAddress, g.data_access)
            recoverPassordLogic.RecoverPassword()
            
            user = User(UserId=recoverPassordLogic.UserId, data_access=g.data_access)
            user.DBFetch(recoverPassordLogic.UserId)
            passwordRecovery = user.PasswordRecovery

            subject = "Password Recovery!"
            sender = "emeeting@jtgd-trust.co.za"
            recipients = [recoverPassordLogic.Email]
            body = "Good day,\n\nPlease click the below link to update your password:\n\n"
            body = body + str(g.domain_name) + str(url_for('resetpassword_view', passwordRecovery=passwordRecovery, email=recoverPassordLogic.Email, sessionGuid=g.session.SessionGuid))[1:]
            body = body + "\n\n"
            body = body + "Regards"
            SendRegistrationEmail(subject=subject, sender=sender, recipients=recipients, body=body)

            flash('Password recovery link sent to your email. Please check your email.', "success")
            resp = make_response(render_template('recoverpassword.html', form=form))
            return resp
        except RecoverPasswordError as recoverpassword_error:
            g.app_has_errors = True
            flash(recoverpassword_error.message, "danger")
            resp = make_response(render_template('recoverpassword.html', form=form))
            return resp

    resp = make_response(render_template('recoverpassword.html', form=form))
    return resp

@app.route("/resetpassword/<string:passwordRecovery>/<string:email>/<string:sessionGuid>", methods=['GET', 'POST'])
def resetpassword_view(passwordRecovery, email, sessionGuid):
    form = ResetPasswordForm()

    if form.validate_on_submit():
        try:
            session = Session(SessionGuid=sessionGuid, data_access=g.data_access)
            session.DBFetchGUID(sessionGuid)

            if session is None: raise FetchError('There is no session associated with your request.')
            
            aes = AESCipher(sysConfig.ENCRYPTION_KEY)
            newPassword = aes.encrypt(form.newPassword.data)

            storedProc = StoredProcs()
            user = storedProc.getUserByPasswordRecovery(passwordRecovery, g.data_access)
            user.Password = newPassword
            user.Save()

            homeForm = HomeForm()

            flash("Password reset successfully. You can now login.", "success")
            resp = make_response(render_template('home.html', form=homeForm))
            return resp
        except FetchError as fetch_error:
            g.app_has_errors = True
            flash(fetch_error.message, "danger")
            resp = make_response(render_template('resetpassword.html', 
                                                 form=form,
                                                 passwordRecovery=passwordRecovery,
                                                 email=email,
                                                 sessionGuid=sessionGuid))
            return resp
        except UpdateError as update_error:
            g.app_has_errors = True
            flash(update_error.message, "danger")
            resp = make_response(render_template('resetpassword.html', 
                                                 form=form,
                                                 passwordRecovery=passwordRecovery,
                                                 email=email,
                                                 sessionGuid=sessionGuid))
            return resp

    resp = make_response(render_template('resetpassword.html', 
                                         form=form,
                                         passwordRecovery=passwordRecovery,
                                         email=email,
                                         sessionGuid=sessionGuid))
    return resp

@app.route("/logout", methods=['GET', 'POST'])
def logout_view(): 
    form = HomeForm()

    # Clear all Session 
    clear_session_variables()
    return redirect(url_for('home_view'))

def clear_session_variables():
    g.session.UserId = 0
    g.session.AdminInd = 0
    g.session.LoggedInInd = 0
    g.session.RememberInd = 0
    g.session.MemberId = None
    g.session.LoggedinEntityName = None
    g.session.Save()
