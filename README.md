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
from flask import abort, Flask, url_for, jsonify, request
from flask_hashids import HashidMixin, Hashids
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# The SECRET_KEY is used as a salt, so don't forget to set this in production
app.config['SECRET_KEY'] = 'secret!'
# Database connection string
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)
hashids = Hashids(app)


class User(HashidMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)


@app.route('/users/', methods=["POST"])
def create_user():
    user = User(**request.json)
    db.session.add(user)
    db.session.commit()
    return 'CREATED', 201


@app.route('/users/')
def get_users():
    users = [
      {
        'id': user.hashid,  # hashid property from HashidMixin
        'name': user.name,
        'url': url_for('get_user', user_id=user.id)  # Int id for url generation
      } for user in User.query.all()
    ]
    return jsonify(users)


@app.route('/users/<hashid:user_id>')
def get_user(user_id):
    # The HashidConverter decodes the given hashid to an int
    user = User.query.get_or_404(user_id)
    return jsonify(
      {
        'id': user.hashid,
        'name':user.name,
        'url': url_for('get_user', user_id=user.id)
      }
    )


@app.route('/users/<hashid:user_id>', methods=["PUT"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    user.name = request.json.get("name",user.name)
    db.session.add(user)
    db.session.commit()
    return 'OK', 200


@app.route('/users/<hashid:user_id>', methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return 'OK', 200


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    app.run()
```

### Running the example app

Start your app with `flask run` and test out the `curl` commands below to see examples on how the hashid works for various CRUD operations.

#### Create a user

```sh
curl \
  -H 'Content-Type: application/json' \
  -X POST \
  -d '{"name": "John Doe"}' \
  localhost:5000/users/
```

```sh
201 CREATED
```

#### Get all users

```sh
curl \
  -H 'Content-Type: application/json' \
  localhost:5000/users/
```

```json
[
  {
    "id":"G8",
    "name":"John",
    "url":"/users/G8"
  }
]
```

#### Get a single user

```sh
curl \
  -H 'Content-Type: application/json' \
  localhost:5000/users/G8
```

```json
{
  "id":"G8",
  "name":"John",
  "url":"/users/G8"
}
```

#### Update a user

```sh
curl \
  -H 'Content-Type: application/json' \
  -X PUT \
  -d '{"name": "Jane Doe"}' \
  localhost:5000/users/G8
```

```sh
200 OK
```

#### Delete a user

```sh
curl \
  -H 'Content-Type: application/json' \
  -X DELETE \
  localhost:5000/users/G8
```

```sh
200 OK
```

## Resources

- https://hashids.org/python/
