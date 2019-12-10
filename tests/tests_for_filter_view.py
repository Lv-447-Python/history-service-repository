"""Module for testing filter view."""
import json
from history_service.views.filter_view import FiltersResource,\
                                              SingleFilterResource
from history_service.views.history_view import HistoryResource
from .tests_for_history_service import HistoryServiceTestCase


class FiltersResourceTestCase(HistoryServiceTestCase):
    """Tests for FiltersResource."""

    def test_filters_getting(self):
        """
        Test for FiltersResource get method.
        Returns:
            None.
        """
        response = self.APP.get('/filter')
        self.assertEqual(response.status_code, 200)


class SingleFilterResourceTestCase(HistoryServiceTestCase):
    """Tests for SingleFilterResource."""

    def test_correct_filter_getting(self):
        """
        Test for SingleFilterResource get method with correct parameters.
        Returns:
            None.
        """
        with open('tests/request_files/correct_history_record_data.json', 'r') as history_json:
            history_content = json.loads(history_json.read())
        response = self.APP.post('/history', json=history_content)
        self.assertEqual(response.status_code, 201)
        response = self.APP.get('/filter/1')
        self.assertEqual(response.status_code, 200)

    def test_incorrect_filter_getting(self):
        """
        Test for SingleFilterResource get method with incorrect parameters.
        Returns:
            None.
        """
        response = self.APP.get('/filter/1')
        self.assertEqual(response.status_code, 400)
