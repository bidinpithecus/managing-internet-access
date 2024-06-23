from flask import render_template, request, redirect, url_for, jsonify
import models
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
        admins = models.Admin.query.all()
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

# @app.route('/switch', methods=['GET', 'POST'])
# def switch():
#     if request.method == 'POST':
#         mac = request.form['mac']
#         ip = request.form['ip']
#         snmp_version = request.form['snmp_version']
#         num_of_ports = request.form['num_of_ports']

#         # Add a new switch in the database

#     if request.method == 'GET':
#         mac = request.form['mac']