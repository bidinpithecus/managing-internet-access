from app import db

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

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
    version = db.Column(db.Integer, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    ports = db.relationship('Port', backref='switch', lazy=True, foreign_keys='Port.switch_mac')

    def to_dict(self):
        return {
            'id': self.id,
            'mac': self.mac,
            'ip': self.ip,
            'version': self.version,
            'size': self.size,
        }

class Port(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    switch_mac = db.Column(db.String(255), db.ForeignKey('switch.mac'))
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'))
    type_id = db.Column(db.Integer, db.ForeignKey('port_type.id'))
    schedules = db.relationship('Scheduling', backref='port', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'number': self.number,
            'switch_mac': self.switch_mac,
            'classroom_id': self.classroom_id,
            'type_id': self.type_id
        }

class PortType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)

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

    def to_dict(self):
        return {
            'id': self.id,
            'start_date': self.start_date.isoformat(),
            'finish_date': self.finish_date.isoformat(),
            'port_id': self.port_id
        }
