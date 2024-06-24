from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, user, password):
        self.user = user
        self.password = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'user': self.user,
            'password': self.password
        }

class Switch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mac = db.Column(db.String(255), unique=True, nullable=False)
    ip = db.Column(db.String(255), unique=True, nullable=False)
    read_community = db.Column(db.String(255), nullable=False)
    write_community = db.Column(db.String(255), nullable=False)
    snmp_version = db.Column(db.Integer, nullable=False)
    num_of_ports = db.Column(db.Integer, nullable=False)
    ports = db.relationship('Port', backref='switch', lazy=True, foreign_keys='Port.switch_id')

    def __init__(self, mac, ip, read_community, write_community, snmp_version, num_of_ports):
        self.mac = mac
        self.ip = ip
        self.read_community = read_community
        self.write_community = write_community
        self.snmp_version = snmp_version
        self.num_of_ports = num_of_ports

    def to_dict(self):
        return {
            'id': self.id,
            'mac': self.mac,
            'ip': self.ip,
            'read_community': self.read_community,
            'write_community': self.write_community,
            'snmp_version': self.snmp_version,
            'num_of_ports': self.num_of_ports,
        }

class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    size = db.Column(db.Integer, nullable=False)

    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'size': self.size
        }

class Port(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    switch_id = db.Column(db.String(255), db.ForeignKey('switch.id'))
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'))
    type_id = db.Column(db.Integer, db.ForeignKey('port_type.id'))
    schedules = db.relationship('Scheduling', backref='port', lazy=True)

    def __init__(self, number, switch_id, classroom_id, type_id):
        self.number = number
        self.switch_id = switch_id
        self.classroom_id = classroom_id
        self.type_id = type_id

    def to_dict(self):
        return {
            'id': self.id,
            'number': self.number,
            'switch_id': self.switch_id,
            'classroom_id': self.classroom_id,
            'type_id': self.type_id
        }

class PortType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, description):
        self.description = description

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description
        }

class Scheduling(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, nullable=False)
    finish_date = db.Column(db.DateTime, nullable=False)
    port_id = db.Column(db.Integer, db.ForeignKey('port.id'), nullable=False)

    def __init__(self, start_date, finish_date, port_id):
        self.start_date = start_date
        self.finish_date = finish_date
        self.port_id = port_id

    def to_dict(self):
        return {
            'id': self.id,
            'start_date': self.start_date.isoformat(),
            'finish_date': self.finish_date.isoformat(),
            'port_id': self.port_id
        }
