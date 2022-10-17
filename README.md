# Flask-Hashids

Hashids integration for Flask applications, it is based on the [Hashid](https://github.com/davidaurelio/hashids-python) package available on [PyPi](https://pypi.org/project/hashids/). With this extension you can conveniently use integer ids for your application logic or database tables and hash them before exposing it in URLs or JSON data.

## Installation

The latest stable version [is available on PyPI](https://pypi.org/project/Flask-Hashids/). Either add `Flask-Hashids` to your `requirements.txt` file or install with pip:

```
pip install Flask-Hashids
```

## Configuration

Flask-Hashids is configured through the standard Flask config API. These are the available options:

- **HASHIDS_ALPHABET**: Read more about that in [Hashids documentation](https://github.com/davidaurelio/hashids-python#using-a-custom-alphabet)
- **HASHIDS_MIN_LENGTH**: Read more about that in [Hashids documentation](https://github.com/davidaurelio/hashids-python#controlling-hash-length)
- **SECRET_KEY**: Used as the salt, read more in [Hashids documentation](https://github.com/davidaurelio/hashids-python#using-a-custom-salt)

## Examples

You can find detailed examples on how to use Flask-Hashids in the examples directory.

### HashidConverter

```python
@app.route('/ressources/<hashid:ressource_id')
def get_ressource(ressource_id: int):
    # The HashidConverter decodes the given hashid to an int
    print(isinstance(ressource_id, int))  # True
    # The HashidConverter encodes the given id to a hashid in the URL
    url_for('get_ressource', ressource_id=123)  # '/ressources/Mj3'
```

### Manual usage

```python
def some_function(ressource_id: int):
    hashid = current_app.extensions['hashids'].encode(123)  # 'Mj3'
    decoded_id = current_app.extensions['hashids'].decode(hashid)  # 123
```


## Resources

- https://hashids.org/python/
