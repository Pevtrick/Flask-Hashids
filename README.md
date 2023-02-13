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
- **HASHIDS_SALT**: It is strongly recommended that this is NEVER the same as the `SECRET_KEY`. Read more about this option in [Hashids documentation](https://github.com/davidaurelio/hashids-python#using-a-custom-salt)

## Examples

You can find more detailed examples on how to use Flask-Hashids in the examples directory.

```python
from flask import Flask, jsonify, url_for
from flask_hashids import HashidMixin, Hashids
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'top_secret_key'
app.config['HASHIDS_SALT'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
db = SQLAlchemy(app)
hashids = Hashids(app)


# The HashidMixin class adds the hashid property which will compute a hashid
# based on the existing id attribute of the instance.
# NOTE: The id attribute must be an int
class User(HashidMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    @property
    def url(self):
        # The HashidConverter encodes the given id to a hashid in the URL
        return url_for('user', user_id=self.id)

    def to_json_serializeable(self):
        return {'id': self.hashid, 'name': self.name, 'url': self.url}


@app.before_first_request
def database_setup():
    db.create_all()
    john = User(name='John')
    db.session.add(john)
    jane = User(name='Jane')
    db.session.add(jane)
    db.session.commit()


@app.route('/users')
def users():
    return [user.to_json_serializeable() for user in User.query.all()], 200


@app.route('/users/<hashid:user_id>')
def user(user_id: int):
    # The HashidConverter decodes the given hashid to an int
    user = User.query.get(user_id)
    if user is None:
        return jsonify('User not found'), 404
    return user.to_json_serializeable(), 200


def main():
    # You can encode and decode hashids manually
    id = 123
    encoded_id = hashids.encode(id)
    decoded_id = hashids.decode(encoded_id)
    app.run()


if __name__ == '__main__':
    main()
```


## Resources

- https://hashids.org/python/
