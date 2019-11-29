"""Module for running Flask app."""
from history_service import APP
from history_service.views.filter_view import FiltersResource, SingleFilterResource
from history_service.views.history_view import HistoryResource, HistoryRecordResource,\
                                               FileHistoryResource, UserHistoryResource


if __name__ == '__main__':
    APP.run(debug=True)
