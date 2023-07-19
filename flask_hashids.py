from flask import current_app, Flask
from hashids import Hashids as _Hashids
from typing import Dict, Optional, Tuple, Union
from werkzeug.routing import BaseConverter, ValidationError


class HashidMixin:
    ''' Hashid Mixin class.

    The HashidMixin class adds a hashid property to a class. This property
    will compute a hashid based on the attribute specified by the class
    variable `__id_attribute__: str = 'id'`.
    
    The class can be used with SQLAlchemy models.
    This won't add a column to the table, the hashid is implemented as a
    property and computed on runtime.

    NOTE: The extended class must have an attribute named after the value of
    `__id_attribute__: str` and must be of type `int`!
    '''

    __id_attribute__: str = 'id'

    @property
    def hashid(self) -> str:
        ''' Hashid property.

        Runtime computed hashid based on the attribute specified by the class
        variable `__id_attribute__: str`.
        '''
        id_attribute: int = getattr(self, self.__class__.__id_attribute__)
        hashids_extension: Hashids = current_app.extensions['hashids']
        return hashids_extension.encode(id_attribute)


class HashidConverter(BaseConverter):
    ''' Hashid Converter.

    Converts and decodes a hashid from routes.\n
    Examples:
        ```python
        @app.route('/resources/<hashid:resource_id')
        def get_resource(resource_id: int):
            print(isinstance(resource_id, int))  # True

        @app.route('/resources/<hashid:resource_ids')
        def get_resources(resource_ids: Tuple[int, ...]):
            print(isinstance(resource_ids, tuple))  # True
            print(all(isinstance(i, int) for i in resource_ids))  # True
        ```

    Converts and encodes values when generating urls.\n
    Examples:
        ```python
        url_for('get_resource', resource_id=123)  # /resources/Mj3

        url_for('get_resource', resource_id=(123, 456))  # /resources/Nk4
        ```
    '''

    def to_python(self, hashid: str) -> Union[int, Tuple[int, ...]]:
        ''' Decodes matched hashid in a URL to an int or tuple of ints '''
        hashids_extension: Hashids = current_app.extensions['hashids']
        decoded_hashid: Union[int, Tuple[int, ...], Tuple[()]] = hashids_extension.decode(hashid)
        if isinstance(decoded_hashid, tuple) and len(decoded_hashid) == 0:
            raise ValidationError()
        return decoded_hashid

    def to_url(self, value: Union[int, Tuple[int, ...]]) -> str:
        ''' Encodes an int or tuple of ints to a hashid when building a URL '''
        hashids_extension: Hashids = current_app.extensions['hashids']
        if isinstance(value, int):
            return hashids_extension.encode(value)
        elif isinstance(value, tuple):
            if len(value) == 0:
                raise ValueError('Tuple must not be empty')
            if not all(isinstance(v, int) for v in value):
                raise TypeError('Tuple must only contain integers')
            return hashids_extension.encode(*value)
        else:
            raise TypeError('Value must be int or tuple of ints')


class Hashids:
    ''' Wrapper class to easily integrate Hashids in Flask '''

    def __init__(self, app: Optional[Flask] = None) -> None:
        self.app: Optional[Flask] = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        ''' Initialize Hashids extension
        
        This method will configure the Hashids extension according to the
        `config` attribute of the passed `app` object. It will also register
        the HashidConverter.
        '''
        hashids_config: Dict = {}
        if 'HASHIDS_ALPHABET' in app.config:
            hashids_config['alphabet']: str = app.config['HASHIDS_ALPHABET']
        if 'HASHIDS_MIN_LENGTH' in app.config:
            hashids_config['min_length']: int = int(app.config['HASHIDS_MIN_LENGTH'])
        if 'HASHIDS_SALT' in app.config:
            hashids_config['salt']: str = app.config['HASHIDS_SALT']
        self._hashids: _Hashids = _Hashids(**hashids_config)
        if not hasattr(app, 'extensions'):
            app.extensions: Dict = {}
        app.extensions['hashids']: Hashids = self
        app.url_map.converters['hashid']: HashidConverter = HashidConverter

    def decode(self, hashid: str) -> Union[int, Tuple[int, ...], Tuple[()]]:
        ''' Decode the passed `hashid`.

        Possible return values:
            - `int` if the hashid contains only one value.
            - `Tuple[int, ...]` if the hashid contains multiple values.
            - `Tuple[()]` if the hashid is invalid.
        '''
        decoded_hashid: Union[Tuple[int, ...], Tuple[()]] = self._hashids.decode(hashid)
        if len(decoded_hashid) == 1:
            return decoded_hashid[0]
        return decoded_hashid

    def encode(self, *values: int) -> str:
        ''' Encode the passed `values`. '''
        return self._hashids.encode(*values)
