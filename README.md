This app is developed on python 3.6 and Flask 0.12

Installation
============
1. install python and pip 
2. pip install -r requirements.txt

Run
=========
On Linux or MacOS, just one command in terminal
>FLASK_APP=main.py flask run
Or you can just run the `main.py` 

APIs available:
=======
### Endpoint : calendar/v1.0/events 
 1. [GET]get all events
 
### Endpoint :calendar/v1.0/events?key=publish_key 
 1. [POST] save a new event, must post with a valid key('publish_key' by default)
            
    
    header: "Content-Type: application/json"
    
    body:{"title":"first from post",
            "details":"still no details",
            "event_start":"2017-03-03 11:50:00", //accept %Y-%m-%d %H:%M:%S  or %Y_%m_%d %H:%M:%S
            "event_end":"2017-03-03 11:50:00", //accept %Y-%m-%d %H:%M:%S  or %Y_%m_%d %H:%M:%S
            "event_owner":"eOhc"
        }
    

### Endpoint : /calendar/v1.0/events/<event_id>
 1. [GET] get an event by id
 2. [DELETE] remove an event by id, when delete a event, you should specify the key by ?key=xxx


### Endpoint: calendar/v1.0/events?date=2017_03_03    //accept %Y_%m_%d or %Y-%m-%d
 1. [GET]get all events for special day
 
 ### Endpoint: calendar/v1.0/daysWithEvent?year=2017&month=3
 1. [GET]get a list of day for the month which have events with them. [1,2,3,21,25]


TODO:
- [x] DateTime in SQLite accept data without time (SQLite store datetime as string.)
- [x] Database return datatime instead of string for event_time(Solved with SQLAlchemy) 
- [x] Authentication 
- [ ] update event api
- [x] use sqlalchemy 
- [x] refine 400 page to json component
- [ ] Code/Structure refactor
- [ ] Write Test
- [ ] Add user and permission control system.
- [ ] Replace simple token based post with user and permission