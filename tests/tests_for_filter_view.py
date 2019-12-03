"""Module for testing filter view."""
import unittest
from history_service import APP, DB
from history_service.views.filter_view import FiltersResource,\
                                              SingleFilterResource


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
        print(response.status_code)
        self.assertEqual(response.status_code, 200)