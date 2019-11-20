"""Module for utils."""
from history_service import DB


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
