"""Module for testing filter view."""
import unittest
import json
from history_service import APP, DB
from history_service.views.filter_view import FiltersResource,\
                                              SingleFilterResource
from history_service.views.history_view import HistoryResource


class HistoryServiceTestCase(unittest.TestCase):

    def setUp(self):
        APP.config['TESTING'] = True
        APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2:' \
                                                '//postgres:postgres@127.0.0.1:5432/HistoryTestDB'
        self.APP = APP.test_client()
        DB.create_all()


class FiltersResourceTestCase(HistoryServiceTestCase):

    def test_filters_getting(self):
        response = self.APP.get('/filter')
        self.assertEqual(response.status_code, 200)


class SingleFilterResourceTestCase(HistoryServiceTestCase):

    def test_correct_filter_getting(self):
        with open('tests/request_files/history_record_create.json', 'r') as history_json:
            history_content = json.loads(history_json.read())
            response = self.APP.post('/history', json=history_content)

        self.assertEqual(response.status_code, 201)


