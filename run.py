"""Module for running Flask app."""
from history_service import app


if __name__ == '__main__':
    app.run(debug=True)
