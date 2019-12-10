"""Module for history service testing."""
import unittest
from history_service import APP, DB

POSTGRES = {
    'user': 'postgres',
    'pw': 'postgres',
    'db': 'HistoryTestDB',
    'host': '127.0.0.1',
    'port': '5432',
}


class HistoryServiceTestCase(unittest.TestCase):
    """General class for service resources testing."""

    def setUp(self):
        """
        Method for app and database configuration.
        Returns:
            None.
        """
        APP.config['TESTING'] = True
        APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2:' \
            '//%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
        self.APP = APP.test_client()
        DB.create_all()

    def tearDown(self):
        """
        Method for database clearing.
        Returns:
            None.
        """
        DB.session.remove()
        DB.drop_all()
