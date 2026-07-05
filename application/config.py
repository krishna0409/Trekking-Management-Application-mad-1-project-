import os 
basedir=os.path.abspath(os.path.dirname(__file__))

class Config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class LocalDevelopmentConfig(Config):
    SQLITE_DB_DIR=os.path.join(basedir,"db_directory")
    SQLALCHEMY_DATABASE_URI= "sqlite:///" + os.path.join(SQLITE_DB_DIR, "database.sqlite3")
    DEBUG=True
    SECRET_KEY="23gfh57betw6gdede6t277"
    SECURITY_PASSWORD_HASH ="bcrypt"
    SECURITY_PASSWORD_SALT ="564GGBDYE782JSBDTG##56H346^"
    SECURITY_REGISTERABLE=True
    SECURITY_SEND_REGISTER_EMAIL=False
    SECURITY_UNAUTHORIZED_VIEW=None
    SECURITY_LOGIN_URL = "/security-login"
    SECURITY_POST_LOGIN_VIEW = "/login"
    SECURITY_LOGIN_USER_TEMPLATE = None