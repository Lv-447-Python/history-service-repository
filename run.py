"""Module for running Flask app."""
from history_service import app
from history_service.views.filter_view import FilterResource
from history_service.views.history_view import HistoryResource


if __name__ == '__main__':
    app.run(debug=True)
