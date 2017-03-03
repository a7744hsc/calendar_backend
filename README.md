This app is developed on python 3.6 and Flask 0.12

Installation
============
1. install python and pip 
2. pip install flask

Run
=========
On Linux or MacOS, just one command in terminal
>FLASK_APP=main.py flask run

APIs available:
=======
### Endpoint : calendar/v1.0/events 
 1. [GET]get all events
 2. [POST] save a new event 
    
    header: "Content-Type: application/json"
    
    body:{"title":"first from post",
            "details":"still no details",
            "event_date":"2017-03-03 11:50:00" //%Y-%m-%d %H:%M:%S
        }
    
 
### Endpoint: calendar/v1.0/events?date=yyyy-mm-dd 
 1. [GET]get all events for special day


TODO:
[x] DateTime in SQLite accept data without time 