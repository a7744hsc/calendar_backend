from main import app as main_app
import unittest
import base64, json
import os
from shutil import copyfile


class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        # self.db_fd, main_app.config['DATABASE'] = tempfile.mkstemp()

        copyfile('test.db', 'temp.db')
        main_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///temp.db'
        self.app = main_app.test_client()
        # with main_app.app_context():
        #     flaskr.init_db()

    def tearDown(self):
        os.remove('temp.db')
        pass
        # os.close(self.db_fd)
        # os.unlink(flaskr.app.config['DATABASE'])

    # Ensure that we can get all events correctly
    def test_get_all_events(self):
        response = self.app.get('/calendar/v1.0/events', headers={
            'Authorization': 'Basic ' + base64.b64encode(bytes("user:passwd", 'utf-8')).decode('utf-8')
        })
        response_str = response.data.decode('unicode_escape')
        res_obj = json.loads(response_str)
        # c = a.decode('utf-8')
        # c1 = a.decode('unicode_escape')
        # print(a.decode('unicode_escape'))
        # d= a.decode('big5')
        # d = a.decode('utf-16')
        # sys.stdout.buffer.write(a)
        getattr(res_obj, 'id', None)

        # self.assertIn(b'You were logged in', response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(res_obj), 6)

    def test_create_multiple_events(self):
        response = self.app.post('/calendar/v1.0/events?key=publish_key', headers={
            'Authorization': 'Basic ' + base64.b64encode(bytes("user:passwd", 'utf-8')).decode('utf-8'),
            'Content-Type': 'application/json'
        }, data=json.dumps({"title": "first from post",
                            "details": "still no details",
                            "event_start": "2017-03-03 11:50:00",
                            "event_end": "2017-03-03 11:50:00",
                            "event_owner": "eOhc",
                            "repeat_times": "2"
                            }))
        response_str = response.data.decode('unicode_escape')
        res_obj = json.loads(response_str)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(res_obj['Success'], 'True')


if __name__ == '__main__':
    unittest.main()
