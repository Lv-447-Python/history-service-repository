"""Module for running Flask app."""
from history_service import APP
from history_service.views.filter_view import FiltersResource
from history_service.views.filter_view import SingleFilterResource
from history_service.views.history_view import HistoryResource
from history_service.views.history_view import HistoryRecordResource
from history_service.views.history_view import DeleteHistoryRecordResource


if __name__ == '__main__':
    APP.run(debug=True)
