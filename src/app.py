from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import *
from snmp.snmp_manager import SNMPManager

db = SQLAlchemy()

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    db.init_app(app)

    snmp_manager = SNMPManager(
        hostname=SnmpConfig.HOSTNAME,
        community_read=SnmpConfig.COMMUNITY_READ_NAME,
        community_write=SnmpConfig.COMMUNITY_WRITE_NAME,
        version=SnmpConfig.VERSION
    )

    return app
