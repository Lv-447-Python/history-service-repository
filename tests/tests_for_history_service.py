import json
import unittest
from history_service import APP, DB


class HistoryServiceTestCase(unittest.TestCase):

    def setUp(self):
        APP.config['TESTING'] = True
        APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2:' \
                                                '//postgres:postgres@127.0.0.1:5432/HistoryTestDB'
        self.APP = APP.test_client()
        DB.create_all()

    def tearDown(self):
        DB.session.remove()
        DB.drop_all()
