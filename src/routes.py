from flask import render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy import text

from snmp.snmp_manager import SNMPManager
from models import *
from app import create_app, db

app = create_app()

@app.route("/", methods = ['GET'])
def index():
    return render_template('index.html')

@app.route('/api/healthcheck', methods=['GET'])
def healthcheck():
    try:
        db.session.execute(text('SELECT 1'))
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "reason": str(e)}), 500

@app.route('/login', methods=['GET'])
def show_login():
    return render_template('login.html')

@app.route('/api/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        password = request.form.get('password')
        if not all([user, password]):
            return jsonify({"message": "Missing data"}), 400

        user = Admin.query.filter_by(user=user).first()
        if user and user.verify_password(password):
            flash("Logged in successfully", "success")
            return redirect(url_for('show_classroom'))
        else:
            flash("Invalid username or password", "error")
            return redirect(url_for('show_login'))
    return render_template('login.html')

@app.route('/signup', methods=['GET'])
def show_signup():
    return render_template('signup.html')

@app.route('/api/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.form
        user = data.get('username')
        password = data.get('password')

        if not all([user, password]):
            return jsonify({"message": "Missing data"}), 400

        existing_user = Admin.query.filter_by(user=user).first()
        if existing_user:
            message = 'Username already taken'
            flash(message)
            return redirect(url_for('login'))

        new_user = Admin(user=user, password=password)
        db.session.add(new_user)
        db.session.commit()

        message = 'Signup successful. Please log in'
        flash(message)
        return redirect(url_for('show_login'))
    return render_template('signup.html')

@app.route('/api/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        data = request.get_json()

        start_date = data.get('start_date')
        finish_date = data.get('finish_date')
        port_id = data.get('port_id')

        if not all([start_date, finish_date, port_id]):
            return jsonify({"message": "Missing data"}), 400

        existing_port = Port.query.filter_by(id=port_id).first()
        if not existing_port:
            return jsonify({"message": "Port unavailable"}), 400

        new_scheduling = Scheduling(
            start_date = start_date,
            finish_date = finish_date,
            port_id = port_id,
        )
        db.session.add(new_scheduling)
        db.session.commit()

        return jsonify({"message": "Schedule added successfully!"}), 201

    elif request.method == 'GET':
        schedules = Scheduling.query.all()
        result_list = [schedule.to_dict() for schedule in schedules]
        return jsonify(result_list), 200

    return jsonify({"message": "Method not allowed"}), 405

@app.route('/switch')
def show_switch():
    return render_template('new-switch.html')

@app.route('/api/switch', methods=['GET', 'POST'])
def switch():
    if request.method == 'POST':
        data = request.form

        mac = data.get('mac')
        ip = data.get('ip')
        read_community = data.get('read_community')
        write_community = data.get('write_community')
        snmp_version = data.get('snmp_version')
        num_of_ports = data.get('num_of_ports')

        classroom_id = data.get('classroom_id')

        if not all([mac, ip, read_community, write_community, snmp_version, num_of_ports, classroom_id]):
            return jsonify({"message": "Missing data"}), 400

        existing_mac = Switch.query.filter_by(mac=mac).first()
        if existing_mac:
            return jsonify({"message": "MAC address already exists"}), 400

        existing_ip = Switch.query.filter_by(ip=ip).first()
        if existing_ip:
            return jsonify({"message": "IP address already exists"}), 400

        classroom: Classroom | None = Classroom.query.filter_by(id=classroom_id).first()
        if not classroom:
            return jsonify({"message": "Classroom not found"}), 400

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

        student_type = PortType.query.filter_by(description="Aluno").first()
        if not student_type:
            return jsonify({"message": "Tipo aluno não adicionado na tabela de tipos de porta"}), 400

        for port_number in range(1, int(num_of_ports) + 1):
            new_port = Port(
                switch_id=new_switch.id,
                number=port_number,
                type_id=student_type.id,
                classroom_id=classroom.id
            )
            db.session.add(new_port)
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

@app.route('/classroom')
def show_classroom():
    return render_template('new-classroom.html')

@app.route('/api/classroom', methods=['GET', 'POST'])
def classroom():
    if request.method == 'POST':
        data = request.form
        name = data.get('classroom-name')

        if not all([name]):
            return jsonify({"message": "Missing data"}), 400

        existing_room = Classroom.query.filter_by(name=name).first()
        if existing_room:
            return jsonify({"message": "Classroom already exists"}), 400

        new_classroom = Classroom(name=name)
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

@app.route('/api/multiple-ports', methods=['POST'])
def handle_ports():
    data = request.get_json()

    professor_port = data.get('professor_port')
    switch_port = data.get('switch_port')
    backend_port = data.get('backend_port')
    other_rooms_ports = data.get('other_rooms_ports', [])

    if professor_port and int(professor_port):
        professor_port = int(professor_port)

    professor_type = PortType.query.filter_by(description="Professor").first()
    if not professor_type:
        return jsonify({"message": "Tipo professor não adicionado na tabela de tipos de porta"}), 400

    port = Port.query.get(professor_port)
    if port:
        port.type_id = professor_type.id
        db.session.commit()

    if switch_port and int(switch_port):
        switch_port = int(switch_port)

    switch_type = PortType.query.filter_by(description="Switch").first()
    if not switch_type:
        return jsonify({"message": "Tipo switch não adicionado na tabela de tipos de porta"}), 400

    port = Port.query.get(switch_port)
    if port:
        port.type_id = switch_type.id
        db.session.commit()

    if backend_port and int(backend_port):
        backend_port = int(backend_port)

    backend_type = PortType.query.filter_by(description="Backend").first()
    if not backend_type:
        return jsonify({"message": "Tipo backend não adicionado na tabela de tipos de porta"}), 400

    port = Port.query.get(backend_port)
    if port:
        port.type_id = backend_type.id
        db.session.commit()

    other_classrooms_ports = []

    for item in other_rooms_ports:
        port_id = int(item.get('port_id'))
        classroom_id = int(item.get('classroom_id'))

        port = Port.query.get(port_id)
        if port:
            port.classroom_id = classroom_id
            db.session.commit()
            other_classrooms_ports.append({'port_id': port_id, 'classroom_id': classroom_id})

    return jsonify({
        'message': 'Ports registered successfully',
        'professor_port': professor_port,
        'switch_port': switch_port,
        'backend_port': backend_port,
        'other_rooms_ports': other_classrooms_ports
    }), 201

@app.route('/api/porttype', methods=['GET', 'POST'])
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

@app.route('/ports')
def show_ports():
    return render_template('new-ports.html')

@app.route('/api/port', methods=['GET', 'POST'])
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

@app.route('/api/first-port-for-switch', methods=['GET', 'POST'])
def first_port():
    if request.method == 'GET':
        switch_id = request.args.get('id')

        if switch_id:
            port = Port.query.filter_by(switch_id=switch_id).order_by(Port.number).first()
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

@app.route('/api/port-status', methods=['GET', 'POST'])
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
