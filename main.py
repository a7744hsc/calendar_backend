from flask import Flask, g, jsonify, request, abort, make_response
from flask_httpauth import HTTPBasicAuth
import os
from datetime import datetime
from db import get_db

app = Flask(__name__)
app.config.from_object(__name__)  # load config from this file , flaskr.py
auth = HTTPBasicAuth()


@app.route('/calendar/v1.0/events', methods=['GET'])
@auth.login_required
def get_events():
    db = get_db(app.config['DATABASE'])
    cur = db.cursor()
    date_str = request.args.get('date')
    if date_str is not None:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        cur.execute("""select id,event_date,title,details from events where date(event_date)=?""", (target_date,))
    else:
        cur.execute("""SELECT id,event_date,title,details from events""")

    results = cur.fetchall()

    return jsonify(results)


@app.route('/calendar/v1.0/events', methods=['POST'])
@auth.login_required
def create_task():
    if not request.json or 'title' not in request.json \
            or 'details' not in request.json or 'event_date' not in request.json:
        abort(400)

    title = request.json['title']
    details = request.json['details']
    try:
        event_date = datetime.strptime(request.json['event_date'], '%Y-%m-%d %H:%M:%S')
    except ValueError:
        abort(400)

    db = get_db(app.config['DATABASE'])
    cur = db.cursor()
    cur.execute(
        """INSERT INTO events ( event_date,created_date,last_modified_date, title, details) VALUES (?,?,?,?,?)""",
        (event_date, datetime.now(), datetime.now(), title, details))
    db.commit()

    return jsonify({'Success': 'True'}), 201


@app.route('/calendar/v1.0/events/<event_id>', methods=['GET'])
@auth.login_required
def get_event_by_id(event_id):
    db = get_db(app.config['DATABASE'])
    cur = db.cursor()
    cur.execute('SELECT id,date,title,details from events;')
    # print(cur.fetchone()['title'])
    results = cur.fetchall()
    print(type(event_id))

    return jsonify(results)


@auth.verify_password
def verify_pw(username, password):
    return username == 'user' and password == 'passwd'


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@app.errorhandler(500)
def internal_error(error):
    return make_response(jsonify({'Error': str(error)}), 500)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'Error': 'Your request could not be understood'}), 400)


@app.teardown_appcontext
def close_db(error):
    print("""Closes the database again at the end of the request.""")
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


# Load default config and override config from an environment variable
app.config.update(dict(
        DATABASE=os.path.join(app.root_path, 'calendar.db'),
        SECRET_KEY='development key',
        USERNAME='admin',
        PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
