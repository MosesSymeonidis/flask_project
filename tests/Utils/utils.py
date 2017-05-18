import unittest
from datetime import datetime
from Utils.utils import *
from bson import objectid
from flask import Flask, current_app
import server

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        server.app.config['TESTING'] = True
        server.app.config['WTF_CSRF_ENABLED'] = False
        self.app = server.app.test_client()


    def tearDown(self):
        pass


    def test_bson_handler(self):
        function = bson_handler

        date = datetime(2017, 1, 1, 0, 0, 0)
        self.assertEquals(date.isoformat(),function(date))

        self.assertEquals ('True', function(True))
        self.assertEquals ('False', function(False))

        object_id = objectid.ObjectId("5916c4e544a7211eed4de9b2")
        self.assertEquals ("5916c4e544a7211eed4de9b2",function(object_id))

        e = Exception()

        self.assertEquals ({
            'error':True,
            'error_str': ''
            }, function(e) )

        general_value = 56
        self.assertEquals ('56', function(general_value))

    def test_json_response(self):
        pass
        # date = datetime(2017, 1, 1, 0, 0, 0)
        #
        # with server.app.app_context():
        #     print(server.app.response_class)
        #
        #     def gen_function():
        #         return {
        #             'id': objectid.ObjectId("5916c4e544a7211eed4de9b2"),
        #             'date': date,
        #             'boolean1': True,
        #             'boolean2': False,
        #             'number': 45,
        #             'number2': 5.5,
        #             'string': 'something',
        #             'nested':{
        #                 'id': objectid.ObjectId("5916c4e544a7211eed4de9b2"),
        #                 'date': date,
        #                 'boolean1': True,
        #                 'boolean2': False,
        #                 'number': 45,
        #                 'number2': 5.5,
        #                 'string': 'something',
        #             }
        #         }
        #     func_test = json_response(gen_function)
        #
        #     print(type(func_test))
        #     resp = func_test().get_data(as_text=True)

    def test_str_import(self):
        self.assertEquals( 'test', str_import('views.test.test').__name__)

        with self.assertRaises(AttributeError):
            str_import('views.test.testasd')


if __name__ == '__main__':
    unittest.main()
