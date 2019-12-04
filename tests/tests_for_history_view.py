"""Module for testing history view."""
import json
from .tests_for_history_service import HistoryServiceTestCase
from history_service.views.history_view import HistoryResource, HistoryRecordResource,\
                                               FileHistoryResource, UserHistoryResource


class HistoryResourceTestCase(HistoryServiceTestCase):
    """Tests for HistoryResource."""

    def test_history_getting(self):
        """
        Test for HistoryResource get method.
        Returns:
            None.
        """
        response = self.APP.get('/history')
        self.assertEqual(response.status_code, 200)

    def test_new_history_record_creation_with_correct_data(self):
        """
        Test for HistoryResource post method with correct data.
        Returns:
            None.
        """
        with open('tests/request_files/history_record_with_correct_data.json', 'r') as history_json:
            history_content = json.loads(history_json.read())
            response = self.APP.post('/history', json=history_content)
        self.assertEqual(response.status_code, 201)

    def test_new_history_record_creation_with_incorrect_keys(self):
        """
        Test for HistoryResource post method with incorrect keys.
        Returns:
            None.
        """
        with open('tests/request_files/history_record_with_incorrect_keys.json', 'r') as history_json:
            history_content = json.loads(history_json.read())
            response = self.APP.post('/history', json=history_content)
        self.assertEqual(response.status_code, 400)

    def test_new_history_record_creation_with_incorrect_values(self):
        """
        Test for HistoryResource post method with incorrect values.
        Returns:
            None.
        """
        with open('tests/request_files/history_record_with_incorrect_values.json', 'r') as history_json:
            history_content = json.loads(history_json.read())
            print(history_content)
            response = self.APP.post('/history', json=history_content)
        self.assertEqual(response.status_code, 400)

    def test_existing_history_record_creation(self):
        """
        Test for HistoryResource post method in case of existing such record.
        Returns:
            None.
        """
        with open('tests/request_files/history_record_with_correct_data.json', 'r') as history_json:
            history_content = json.loads(history_json.read())
            response = self.APP.post('/history', json=history_content)
        self.assertEqual(response.status_code, 201)
        response = self.APP.post('/history', json=history_content)
        self.assertEqual(response.status_code, 409)


class HistoryRecordResourceTestCase(HistoryServiceTestCase):
    """Tests for HistoryRecordResource."""

    def test_history_record_getting_with_correct_parameters(self):
        """
        Test for HistoryRecordResource get method with correct parameters.
        Returns:
            None.
        """
        with open('tests/request_files/history_record_with_correct_data.json', 'r') as history_json:
            history_content = json.loads(history_json.read())
            response = self.APP.post('/history', json=history_content)
        self.assertEqual(response.status_code, 201)
        response = self.APP.get('history/user/2/file/1/filter/1')
        self.assertEqual(response.status_code, 200)

    def test_history_record_getting_with_incorrect_parameters(self):
        """
        Test for HistoryRecordResource get method with incorrect parameters.
        Returns:
            None.
        """
        with open('tests/request_files/history_record_with_correct_data.json', 'r') as history_json:
            history_content = json.loads(history_json.read())
            response = self.APP.post('/history', json=history_content)
        self.assertEqual(response.status_code, 201)
        response = self.APP.get('history/user/2/file/2/filter/3')
        self.assertEqual(response.status_code, 400)
