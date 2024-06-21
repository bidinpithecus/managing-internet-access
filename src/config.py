class DevelopmentConfig(object):
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = 'do-i-really-need-this'
    FLASK_HTPASSWD_PATH = '/secret/.htpasswd'
    FLASK_SECRET = SECRET_KEY
    DB_HOST = 'postgresdb'
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:admin@localhost:5432/snmp_manager'

class ProductionConfig(DevelopmentConfig):
    DEVELOPMENT = False
    DEBUG = False
    DB_HOST = 'database'

class SnmpConfig:
    HOSTNAME = '10.90.90.90'
    VERSION = 1
    COMMUNITY_READ_NAME = 'public'
    COMMUNITY_WRITE_NAME = 'private'
