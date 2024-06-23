from flask import render_template, request, redirect, url_for, jsonify
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

@app.route('/mara', methods=['GET'])
def test():
    try:
        admins = Admin.query.all()
        result_list = [admin.to_dict() for admin in admins]

        return jsonify(result_list), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "reason": str(e)}), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Auth

        return redirect(url_for('dashboard'))
    return render_template('login.html')

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
