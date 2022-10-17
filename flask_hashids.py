from flask import abort, current_app, Flask
from hashids import Hashids as _Hashids
from typing import Any, Dict
from werkzeug.routing import BaseConverter


class HashidMixin:
    '''
    Hashid mixin meant for use with SQLAlchemy models.
    Adds a property to the model which returns a hashid based on the model id.

    This won't add a column to the model, the hashid is computed on runtime.

    Note: The extended class must have an attribute 'id' of type int!
    '''
    @property
    def hashid(self) -> str:
        return current_app.extensions['hashids'].encode(self.id)


class HashidConverter(BaseConverter):
    '''
    Hashid Converter.

    Converts given hashids from routes to integers.
    Example:
        @bp.route('/users/<hashid:user_id')
        def my_route(user_id: int):
            print(isinstance(user_id, int))  # True

    Converts integers to hashids when generating urls.
    Example:
        url_for('users.user', user_id=123)  # /users/Mj3
    '''

    def to_python(self, value: str) -> int:
        try:
            decoded_value = current_app.extensions['hashids'].decode(value)
        except IndexError:
            abort(404)
        return decoded_value

    def to_url(self, value: int) -> str:
        return current_app.extensions['hashids'].encode(value)


class Hashids:
    ''' Wrapper class to easily integrate hashids in Flask '''

    def __init__(self, app: Flask = None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        ''' Setup Hashids, includes the integration of the HashidConverter. '''
        hashids_config: Dict[str, Any] = {}
        if 'HASHIDS_ALPHABET' in app.config:
            hashids_config['alphabet'] = app.config['HASHIDS_ALPHABET']
        if 'HASHIDS_MIN_LENGTH' in app.config:
            hashids_config['min_length'] = \
                int(app.config['HASHIDS_MIN_LENGTH'])
        if 'SECRET_KEY' in app.config:
            hashids_config['salt'] = app.config['SECRET_KEY']
        self._hashids = _Hashids(**hashids_config)
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['hashids'] = self
        app.url_map.converters['hashid'] = HashidConverter

    def decode(self, value: str) -> int:
        ''' Decode a hashid to an integer. '''
        return self._hashids.decode(value)[0]

    def encode(self, value: int) -> str:
        ''' Encode an integer to a hashid. '''
        return self._hashids.encode(value)
