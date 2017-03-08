from main import app as main_app
import unittest
import base64, json
import os,sys
import tempfile


class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        # self.db_fd, main_app.config['DATABASE'] = tempfile.mkstemp()
        main_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = main_app.test_client()
        # with main_app.app_context():
        #     flaskr.init_db()

    def tearDown(self):
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
        getattr(res_obj,'id',None)

        # self.assertIn(b'You were logged in', response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(res_obj), 6)


if __name__ == '__main__':
    unittest.main()
