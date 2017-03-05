This app is developed on python 3.6 and Flask 0.12

Installation
============
1. install python and pip 
2. pip install flask flask-httpauth

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
            "event_date":"2017-03-03 11:50:00" //accept %Y-%m-%d %H:%M:%S  or %Y_%m_%d %H:%M:%S  
        }
    
 
### Endpoint: calendar/v1.0/events?date=2017_03_03    //accept %Y_%m_%d or %Y-%m-%d
 1. [GET]get all events for special day


TODO:
- [ ] DateTime in SQLite accept data without time 
- [ ] Database return datatime instead of string for event_time 
- [x] Authentication 
- [ ] update event api
- [ ] use sqlalchemy 
- [x] refine 400 page to json component
- [ ] Code/Structure refactor
- [ ] Write Test