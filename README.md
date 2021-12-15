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

```python
from flask import abort, Flask, render_template, url_for
from flask_hashids import HashidMixin, Hashids
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# The SECRET_KEY is used as a salt, so don't forget to set this in production
app.config['SECRET_KEY'] = 'secret!'
db = SQLAlchemy(app)
hashids = Hashids(app)


class User(HashidMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)


@app.route('/users')
def users():
    hashid_users = [
      {
        'id': user.hashid,  # hashid property from HashidMixin
        'name': user.name,
        'url': url_for('user', user_id=user.id)  # Int id for url generation
      } for user in User.query.all()
    ]
    return render_template('users.html', users=hashid_users)


@app.route('/users/<hashid:user_id>')
def user(user_id):
    # The HashidConverter decodes the given hashid to an int
    user = User.query.get_or_404(user_id):
    return render_template('user.html', user=user)


if __name__ == '__main__':
    app.run()
```


## Ressources

- https://hashids.org/python/
