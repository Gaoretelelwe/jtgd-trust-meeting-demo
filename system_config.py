import os

class SystemConfig():
    
    def __init__(self):

        # Persistent Environment Variables

        # Application Configs
        self.APP_SECRET_KEY = '3Md6Ef4E5Ta5Ifc1N2G4J4T5Gdbac2Df5T9Rc3Ub6Sc7Tcb1' # str(os.environ.get('JTGD_TRUST_APP_SECRET_KEY')) # 
        #self.APP_UPLOAD_FOLDER = 'Documents/Uploads/' # str(os.environ.get('JTGD_TRUST_APP_UPLOAD_FOLDER')) # 
        self.APP_UPLOAD_FOLDER = 'static/docs/' # str(os.environ.get('JTGD_TRUST_APP_UPLOAD_FOLDER')) # 
        self.APP_TEMPLATE_FOLDER = 'Web/Template' # str(os.environ.get('JTGD_TRUST_APP_TEMPLATE_FOLDER')) # 
        self.APP_MAX_CONTENT_LENGTH = 16 * 1024 * 1024
        self.APP_ALLOWED_EXTENSION = set(['pdf', 'png', 'jpg', 'jpeg', 'doc']) # {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

        # Database Configs
        self.DATABASE_USERNAME = 'boyghtdq_KopanoAdmin' # str(os.environ.get('JTGD_TRUST_DATABASE_USERNAME')) # 'ogoyfsjp_jtgdtrust' # 'ogoyfsjp' # 'ogoyfsjp_vendorguy' # os.environ.get('JTGD_TRUST_DATABASE_USERNAME') # os.environ.get('TUELO_PAY_DB_USERNAME') # 
        self.DATABASE_PASSWORD = 'K0pan0Adm1n' # str(os.environ.get('JTGD_TRUST_DATABASE_PASSWORD')) # 'G0ldc@t91' # os.environ.get('TUELO_PAY_DB_PASSWORD') # 
        self.DATABASE_HOST = 'cp-2.hkdns.co.za' # str(os.environ.get('JTGD_TRUST_DATABASE_HOST')) # 'cp-7.hkdns.co.za' # 'cp28-za1.host-ww.net' # os.environ.get('TUELO_PAY_DB_HOST') # 
        self.DATABASE_PORT = '3306' # str(os.environ.get('JTGD_TRUST_DATABASE_PORT')) # os.environ.get('TUELO_PAY_DB_PORT') # 
        #self.DATABASE_NAME = 'boyghtdq_Kopano' # 'boyghtdq_Muuzaji_Demo' # str(os.environ.get('JTGD_TRUST_DATABASE_NAME')) # 'boyghtdq_xjbcirqc_Muuzaji' # 'ogoyfsjp_Muuzaji' # os.environ.get('TUELO_PAY_DB_DATABASE') #
        self.DATABASE_NAME = 'boyghtdq_Kopano_PROD' #'boyghtdq_Muuzaji_Demo' # str(os.environ.get('JTGD_TRUST_DATABASE_NAME')) # 'boyghtdq_xjbcirqc_Muuzaji' # 'ogoyfsjp_Muuzaji' # os.environ.get('TUELO_PAY_DB_DATABASE') #

        # Email Configs
        self.REGISTRATION_MAIL_SERVER = 'jtgd-trust.co.za' # str(os.environ.get('JTGD_TRUST_REGISTRATION_MAIL_SERVER')) # 'mail.tuelopay.co.za' # 
        self.REGISTRATION_MAIL_PORT = 465
        self.REGISTRATION_MAIL_USE_SSL = True
        self.REGISTRATION_MAIL_USERNAME = 'emeeting@jtgd-trust.co.za' # 'registrations@vendors.jtgd-trust.co.za' # str(os.environ.get('JTGD_TRUST_REGISTRATION_MAIL_USERNAME')) # 'gaoretelelwe@tuelopay.co.za' # 
        self.REGISTRATION_MAIL_PASSWORD = '3M33t1n9@Jt' # 'V3nd0R9uy' # str(os.environ.get('JTGD_TRUST_REGISTRATION_MAIL_PASSWORD')) # 'G0ldc@t91' # 
        self.REGISTRATION_MAIL_SENDER = ('JTGD EMEETING', 'emeeting@jtgd-trust.co.za')

        self.NOTIFICATIONS_MAIL_SERVER = 'jtgd-trust.co.za' # str(os.environ.get('JTGD_TRUST_NOTIFICATIONS_MAIL_SERVER')) # 'mail.tuelopay.co.za' # os.environ.get('JTGD_TRUST_MAIL_SERVER') # 
        self.NOTIFICATIONS_MAIL_PORT = 465
        self.NOTIFICATIONS_MAIL_USE_SSL = True
        self.NOTIFICATIONS_MAIL_USERNAME = 'emeeting@jtgd-trust.co.za' # 'vendors@jtgd-trust.co.za' # str(os.environ.get('JTGD_TRUST_NOTIFICATIONS_MAIL_USERNAME')) # 'gaoretelelwe@tuelopay.co.za' # os.environ.get('JTGD_TRUST_MAIL_USERNAME') # 
        self.NOTIFICATIONS_MAIL_PASSWORD = '3M33t1n9@Jt' # 'V3nd0R9uy@jt9D' # str(os.environ.get('JTGD_TRUST_NOTIFICATIONS_MAIL_PASSWORD')) # 'G0ldc@t91' # os.environ.get('JTGD_TRUST_MAIL_PASSWORD') # 
        self.NOTIFICATIONS_MAIL_SENDER = ('JTGD EMEETING', 'emeeting@jtgd-trust.co.za')

        # export JTGD_TRUST_APP_SECRET_KEY='3d6f45a5fc12445dbac2f59c3b6c7cb1'
        # export JTGD_TRUST_APP_UPLOAD_FOLDER='Documents/uploads/'
        # export JTGD_TRUST_APP_TEMPLATE_FOLDER='Web/Template'

        # export JTGD_TRUST_DATABASE_USERNAME='boyghtdq_boyghtdq'
        # export JTGD_TRUST_DATABASE_PASSWORD='V3nd0R9uy'
        # export JTGD_TRUST_DATABASE_HOST='cp-2.hkdns.co.za'
        # export JTGD_TRUST_DATABASE_PORT='3306'
        # export JTGD_TRUST_DATABASE_NAME='boyghtdq_Muuzaji_Demo'

        # export JTGD_TRUST_REGISTRATION_MAIL_SERVER='vendors.jtgd-trust.co.za'
        # export JTGD_TRUST_REGISTRATION_MAIL_USERNAME='registrations@vendors.jtgd-trust.co.za'
        # export JTGD_TRUST_REGISTRATION_MAIL_PASSWORD='V3nd0R9uy'

        # export JTGD_TRUST_NOTIFICATIONS_MAIL_SERVER='jtgd-trust.co.za'
        # export JTGD_TRUST_NOTIFICATIONS_MAIL_USERNAME='vendors@jtgd-trust.co.za'
        # export JTGD_TRUST_NOTIFICATIONS_MAIL_PASSWORD='V3nd0R9uy@jt9D'

        # export JTGD_TRUST_APP_ENCRYPTION_KEY = '5tr0n9P@55w0rd4LIFE'


        # Email - vendors@jtgd-trust.co.za
        # V3nd0R9uy@jt9D

        # Encryption Key

        self.ENCRYPTION_KEY = '5tr0n9P@55w0rd4LIFE' #str(os.environ.get('JTGD_TRUST_APP_ENCRYPTION_KEY')) # 
        # export JTGD_TRUST_APP_ENCRYPTION_KEY='5tr0n9P@55w0rd4LIFE'

        # export JTGD_TRUST_DATABASE_NAME='boyghtdq_xjbcirqc_Muuzaji'







        #import pdb
        #pdb.set_trace()

        # Site Configs


        # COMMANDS TO RUN
        # export APP_SECRET_KEY='3d6f45a5fc12445dbac2f59c3b6c7cb1'
        # export APP_UPLOAD_FOLDER='Documents/uploads/'
        # export APP_TEMPLATE_FOLDER='Web/Template'





        # export JTGD_TRUST_
        # export JTGD_TRUST_
        # JTGD_TRUST_DATABASE_USERNAME='ogoyfsjp' export JTGD_TRUST_DATABASE_USERNAME
        # JTGD_TRUST_DATABASE_PASSWORD='G0ldc@t91' export JTGD_TRUST_DATABASE_PASSWORD
        # JTGD_TRUST_DATABASE_HOST='cp-7.hkdns.co.za' export JTGD_TRUST_DATABASE_HOST
        # JTGD_TRUST_DATABASE_PORT='3306' export JTGD_TRUST_DATABASE_PORT
        # JTGD_TRUST_DATABASE_NAME='ogoyfsjp_Muuzaji' export JTGD_TRUST_DATABASE_NAME
        # export JTGD_TRUST_MAIL_SERVER='mail.tuelopay.co.za'
        # export JTGD_TRUST_MAIL_PORT=465
        # export JTGD_TRUST_MAIL_USE_SSL=True
        # export JTGD_TRUST_MAIL_USERNAME='gaoretelelwe@tuelopay.co.za'
        # export JTGD_TRUST_MAIL_PASSWORD='G0ldc@t91'

        # set 
        # -- above return env. variables

        #echo
        # -- eg echo $JTGD_TRUST_APP_SECRET_KEY




