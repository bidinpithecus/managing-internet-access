from flask import render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy import text

from snmp.snmp_manager import SNMPManager
from models import *
from app import create_app, db

app = create_app()

@app.route("/", methods = ['GET'])
def index():
    return render_template('index.html')

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    try:
        db.session.execute(text('SELECT 1'))
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "reason": str(e)}), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        user = data.get('user')
        password = data.get('password')

        if not all([user, password]):
            return jsonify({"message": "Missing data"}), 400

        user = Admin.query.filter_by(user=user).first()
        if user and user.verify_password(password):
            message = 'Logged in successfully'
            flash(message)
            return jsonify({"message": message}), 200
        else:
            message = 'Invalid username or password'
            flash(message)
            return jsonify({"message": message}), 401
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        user = data.get('user')
        password = data.get('password')

        if not all([user, password]):
            return jsonify({"message": "Missing data"}), 400

        existing_user = Admin.query.filter_by(user=user).first()
        if existing_user:
            message = 'Username already taken'
            flash(message)
            return jsonify({"message": message}), 401

        new_user = Admin(user=user, password=password)
        db.session.add(new_user)
        db.session.commit()

        message = 'Signup successful. Please log in'
        flash(message)
        return jsonify({"message": message}), 200
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/schedule', methods=['POST'])
def schedule():
    # Schedule block/unblock ports

    return redirect(url_for('dashboard'))

@app.route('/switch', methods=['GET', 'POST'])
def switch():
    if request.method == 'POST':
        data = request.get_json()

        mac = data.get('mac')
        ip = data.get('ip')
        read_community = data.get('read_community')
        write_community = data.get('write_community')
        snmp_version = data.get('snmp_version')
        num_of_ports = data.get('num_of_ports')

        if not all([mac, ip, read_community, write_community, snmp_version, num_of_ports]):
            return jsonify({"message": "Missing data"}), 400

        existing_mac = Switch.query.filter_by(mac=mac).first()
        if existing_mac:
            return jsonify({"message": "MAC address already exists"}), 400

        existing_ip = Switch.query.filter_by(ip=ip).first()
        if existing_ip:
            return jsonify({"message": "IP address already exists"}), 400

        new_switch = Switch(
            mac=mac,
            ip=ip,
            read_community=read_community,
            write_community=write_community,
            snmp_version=snmp_version,
            num_of_ports=num_of_ports
        )
        db.session.add(new_switch)
        db.session.commit()

        return jsonify({"message": "Switch added successfully!"}), 201

    elif request.method == 'GET':
        ip = request.args.get('ip')

        if ip:
            switch = Switch.query.filter_by(ip=ip).first()
            if switch:
                result = switch.to_dict()
                return jsonify(result), 200
            else:
                return jsonify({"message": "Switch not found"}), 404
        else:
            switches = Switch.query.all()
            result_list = [switch.to_dict() for switch in switches]
            return jsonify(result_list), 200

    return jsonify({"message": "Method not allowed"}), 405

@app.route('/classroom', methods=['GET', 'POST'])
def classroom():
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        size = data.get('size')

        if not all([name, size]):
            return jsonify({"message": "Missing data"}), 400

        existing_room = Classroom.query.filter_by(name=name).first()
        if existing_room:
            return jsonify({"message": "Classroom already exists"}), 400

        new_classroom = Classroom(name=name, size=size)
        db.session.add(new_classroom)
        db.session.commit()

        return jsonify({"message": "Classroom added successfully!"}), 201

    elif request.method == 'GET':
        classroom_name = request.args.get('name')

        if classroom_name:
            classroom = Classroom.query.filter_by(name=classroom_name).first()
            if classroom:
                result = classroom.to_dict()
                return jsonify(result), 200
            else:
                return jsonify({"message": "Classroom not found"}), 404
        else:
            classrooms = Classroom.query.all()
            result_list = [classroom.to_dict() for classroom in classrooms]
            return jsonify(result_list), 200

    return jsonify({"message": "Method not allowed"}), 405

@app.route('/porttype', methods=['GET', 'POST'])
def porttype():
    if request.method == 'POST':
        data = request.get_json()
        description = data.get('description')

        if not description:
            return jsonify({"message": "Missing data"}), 400

        existing_type = PortType.query.filter_by(description=description).first()
        if existing_type:
            return jsonify({"message": "Port type already exists"}), 400

        new_porttype = PortType(description=description)
        db.session.add(new_porttype)
        db.session.commit()

        return jsonify({"message": "Port type added successfully!"}), 201

    elif request.method == 'GET':
        description = request.args.get('description')

        if description:
            porttype = PortType.query.filter_by(description=description).first()
            if porttype:
                result = porttype.to_dict()
                return jsonify(result), 200
            else:
                return jsonify({"message": "Port type not found"}), 404
        else:
            porttypes = PortType.query.all()
            result_list = [porttype.to_dict() for porttype in porttypes]
            return jsonify(result_list), 200

    return jsonify({"message": "Method not allowed"}), 405

@app.route('/port', methods=['GET', 'POST'])
def port():
    if request.method == 'POST':
        data = request.get_json()
        number = data.get('number')
        switch_id = data.get('switch_id')
        classroom_id = data.get('classroom_id')
        type_id = data.get('type_id')

        if not all([number, switch_id, classroom_id, type_id]):
            return jsonify({"message": "Missing data"}), 400

        switch = Switch.query.get(switch_id)
        if not switch:
            return jsonify({"message": "Switch not found"}), 404

        classroom = Classroom.query.get(classroom_id)
        if not classroom:
            return jsonify({"message": "Classroom not found"}), 404

        port_type = PortType.query.get(type_id)
        if not port_type:
            return jsonify({"message": "Port type not found"}), 404

        new_port = Port(number=number, switch_id=switch_id, classroom_id=classroom_id, type_id=type_id)
        db.session.add(new_port)
        db.session.commit()

        return jsonify({"message": "Port added successfully!"}), 201

    elif request.method == 'GET':
        port_id = request.args.get('id')

        if port_id:
            port = Port.query.get(port_id)
            if port:
                result = port.to_dict()
                return jsonify(result), 200
            else:
                return jsonify({"message": "Port not found"}), 404
        else:
            ports = Port.query.all()
            result_list = [port.to_dict() for port in ports]
            return jsonify(result_list), 200

    return jsonify({"message": "Method not allowed"}), 405

@app.route('/port-status', methods=['GET', 'POST'])
def port_status():
    if request.method == 'POST':
        data = request.get_json()
        port_id = data.get('port_id')
        status_code = data.get('status_code')

        if not all([port_id, status_code]):
            return jsonify({"message": "Missing data"}), 400

        port = Port.query.get(port_id)
        if not port:
            return jsonify({"message": "Port not found"}), 404

        description = "Aluno"
        port_type = PortType.query.filter_by(description=description).first()

        if not port_type:
            return jsonify({"message": description + " not added to the port_type table"}), 404

        if port.type_id != port_type.id:
            return jsonify({"message": "Port not allowed"}), 401

        switch = Switch.query.get(port.switch_id)
        if not switch:
            return jsonify({"message": "Switch not found"}), 404

        snmp_manager = SNMPManager(switch.hostname, switch.community_read, switch.community_write, switch.version)
        ret = snmp_manager.change_port_status(port.number, status_code)

        if ret:
            return jsonify({"message": "Port status changed successfully"}), 201
        else:
            return jsonify({"message": "Port status unchanged"}), 500

    if request.method == 'GET':
        switch_id = request.args.get('switch_id')
        if not switch_id:
            return jsonify({"message": "Missing switch_id"}), 400

        switch = Switch.query.get(switch_id)
        if not switch:
            return jsonify({"message": "Switch not found"}), 404

        ports = Port.query.filter_by(switch_id=switch_id).all()
        if not ports:
            return jsonify({"message": "Switch has no ports"}), 404

        snmp_manager = SNMPManager(switch.hostname, switch.community_read, switch.community_write, switch.version)
        ret = snmp_manager.get_port_status()

        return jsonify(ret), 200

    return jsonify({"message": "Method not allowed"}), 405
