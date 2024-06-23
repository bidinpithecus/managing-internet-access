from flask import render_template, request, redirect, url_for, jsonify, flash
from models import *
from app import create_app, db
from sqlalchemy import text

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
