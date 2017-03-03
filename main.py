from flask import Flask, g, jsonify, request, abort, make_response
import os
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.config.from_object(__name__)  # load config from this file , flaskr.py


@app.route('/calendar/v1.0/events', methods=['GET'])
def hello_world():
    db = get_db();
    cur = db.cursor();
    date = request.args.get('date')
    if date is not None:
        cur.execute("""select id,event_date,title,details from events where date(event_date)=?""", (date,))
    else:
        cur.execute("""SELECT id,event_date,title,details from events""")

    print(date)
    results = cur.fetchall()
    print(results)

    return jsonify(results)


@app.route('/calendar/v1.0/events', methods=['POST'])
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

    db = get_db()
    cur = db.cursor()
    cur.execute("""INSERT INTO events ( event_date,created_date,last_modified_date, title, details) VALUES (?,?,?,?,?)""",
                (event_date, datetime.now(), datetime.now(), title, details))
    db.commit()


    return jsonify({'Success': 'True'}), 201

@app.route('/calendar/v1.0/events/<event_id>', methods=['GET'])
def get_event_by_id(event_id):
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT id,date,title,details from events;')
    # print(cur.fetchone()['title'])
    results = cur.fetchall()
    print(type(event_id))

    return jsonify(results)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def connect_db():
    print("""Connects to the specific database.""")
    rv = sqlite3.connect(app.config['DATABASE'])
    # rv.row_factory = sqlite3.Row
    rv.row_factory = dict_factory

    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'Error': 'Your request could not be understood'}), 400)


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
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
