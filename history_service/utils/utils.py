"""Module for utils."""
from flask import jsonify
from history_service import DB


def jsonify_data(data, errors, status_code):
    """
    Creates a format JSON representation of data.
    Args:
        data: Response data.
        errors: Message about errors.
        status_code: HTTP status code.
    Returns:
        Formatted JSON.
    """
    return jsonify({
        'data': data,
        'errors': errors,
        'status': status_code
    })


def save_into_db(model_object):
    """
    Function for object saving into database.
    Args:
        model_object:
            Any object of Filter and History classes.
    Returns:
        None.
    """
    DB.session.add(model_object)
    DB.session.commit()


def delete_from_db(model_object):
    """
    Function for object deleting from database.
    Args:
        model_object:
            Any object of Filter and History classes.
    Returns:
        None.
    """
    DB.session.delete(model_object)
    DB.session.commit()
