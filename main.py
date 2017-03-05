from flask import Flask, g, jsonify, request, abort, make_response
from flask_httpauth import HTTPBasicAuth
import os
from datetime import datetime
from db import get_db
from utils import parse_date, parse_datetime

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
        target_date = parse_date(date_str)
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
    event_dt = parse_datetime(request.json['event_date'])

    db = get_db(app.config['DATABASE'])
    cur = db.cursor()
    cur.execute(
            """INSERT INTO events ( event_date,created_date,last_modified_date, title, details) VALUES (?,?,?,?,?)""",
            (event_dt, datetime.now(), datetime.now(), title, details))
    db.commit()

    return jsonify({'Success': 'True'}), 201


@app.route('/calendar/v1.0/daysWithEvent', methods=['GET'])
@auth.login_required
def get_date():
    try:
        year = request.args.get('year')
        month = request.args.get('month')
        date = datetime(int(year), int(month), 3)
        date_str = date.strftime('%Y%m')
    except Exception:
        abort(400)

    db = get_db(app.config['DATABASE'])
    cur = db.cursor()
    cur.execute(
            """select id,event_date from events WHERE strftime('%Y%m', event_date) = ?""",
            (date_str,))
    results = cur.fetchall()

    days_with_event = set()
    for evt in results:
        days_with_event.add(datetime.strptime(evt['event_date'], '%Y-%m-%d %H:%M:%S').day)

    return jsonify(list(days_with_event))


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
    return make_response(jsonify({'Error': str(error)}), 400)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'Error': 'Your request could not be understood'}), 400)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        print("""Closes the database again at the end of the request.""")
        g.sqlite_db.close()


# Load default config and override config from an environment variable
app.config.update(dict(
        DATABASE=os.path.join(app.root_path, 'calendar.db'),
        SECRET_KEY='development key',
        USERNAME='admin',
        PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
