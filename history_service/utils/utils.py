"""Module for utils."""
import json
from history_service import DB
from history_service.serializers.filter_serializer import FilterSchema
from history_service.serializers.history_serializer import HistorySchema


def dump_filter_object(filter_object):
    """
    Method for filter object serialization.
    Args:
        filter_object:
            Any instance of Filter model class.
    Returns:
        Formatted data presentation.
    """
    filter_serializer = FilterSchema()
    filter_value = filter_serializer.dump(filter_object)
    filter_value['filter_data'] = json.loads(filter_value['filter_data'])
    return filter_value


def load_filter_object(filter_value):
    """
    Method for filter object deserialization and validation.
    Args:
        filter_value:
            Input dictionary.
    Returns:
        Filter model instance.
    """
    filter_serializer = FilterSchema()
    filter_object = filter_serializer.load(filter_value)
    return filter_object


def dump_history_object(history_object):
    """
    Method for history object serialization.
    Args:
        history_object:
            Any instance of History model class.
    Returns:
        Formatted data presentation.
    """
    history_serializer = HistorySchema()
    history = history_serializer.dump(history_object)
    history['rows_id'] = json.loads(history['rows_id'])
    return history


def load_history_object(history):
    """
    Method for history object deserialization and validation.
    Args:
        history:
            Input dictionary.
    Returns:
        History model instance.
    """
    history_serializer = HistorySchema()
    history_object = history_serializer.load(history)
    return history_object


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
