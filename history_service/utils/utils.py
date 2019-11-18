from flask import jsonify


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
