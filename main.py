from flask import Flask, g, jsonify, request, abort, make_response
from CustomJSONEncoder import CustomJSONEncoder
from flask_httpauth import HTTPBasicAuth
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from utils import parse_date, parse_datetime
import os
from sqlalchemy import func, and_, extract

app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
        DATABASE=os.path.join(app.root_path, 'calendar.db'),
        SQLALCHEMY_DATABASE_URI='sqlite:///calendar.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=False,
        SECRET_KEY='development key',
))
app.json_encoder = CustomJSONEncoder
auth = HTTPBasicAuth()
db_alchemy = SQLAlchemy(app)
from models import *


@app.route('/calendar/v1.0/events', methods=['GET'])
@auth.login_required
def get_events():
    date_str = request.args.get('date')
    if date_str is not None:
        target_date = parse_date(date_str)
        qresults = db_alchemy.session.query(Event).filter(func.date(Event.event_start) == target_date).all()
        results = []
        for r in qresults:
            di = r.as_dict()
            di['event_start'] = di['event_start'].strftime('%H:%M:%S')
            di['event_end'] = di['event_end'].strftime('%H:%M:%S')
            results.append(di)
    else:
        qresults = Event.query.all()
        results = [r.as_dict() for r in qresults]

    return jsonify(results)
    # if getattr(results[0],'as_dict', None):
    # return jsonify([r.as_dict() for r in results])


@app.route('/calendar/v1.0/events', methods=['POST'])
@auth.login_required
def create_task():
    print(request.args.get('key'))
    if request.args.get('key') != 'publish_key':
        abort(401)

    if not request.json or 'title' not in request.json or 'event_owner' not in request.json \
            or 'details' not in request.json or 'event_start' not in request.json or 'event_end' not in request.json:
        abort(400)

    title = request.json['title']
    details = request.json['details']
    start_dt = parse_datetime(request.json['event_start'])
    end_dt = parse_datetime(request.json['event_end'])
    owner = request.json['event_owner']
    evt = Event(event_start=start_dt, event_end=end_dt, created_date=datetime.now(), last_modified_date=datetime.now(),
                event_owner=owner, title=title, details=details)
    db_alchemy.session.add(evt)
    db_alchemy.session.commit()

    return jsonify({'Success': 'True', 'event': evt.as_dict()}), 201


@app.route('/calendar/v1.0/daysWithEvent', methods=['GET'])
@auth.login_required
def get_date():
    try:
        year = request.args.get('year')
        month = request.args.get('month')
    except Exception:
        abort(400)
    results = Event.query.filter(and_(extract('year', Event.event_start) == year,
                                      extract('month', Event.event_start) == month)).all()
    days_with_event = set()
    for evt in results:
        days_with_event.add(evt.event_start.day)
    return jsonify(list(days_with_event))


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


@app.errorhandler(401)
def bad_request(error):
    return make_response(jsonify({'Error': 'Unauthorized access'}), 401)


@app.teardown_appcontext
def close_db(error):
    pass


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
