from flask import Flask, jsonify, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_hashids import HashidMixin, Hashids
from werkzeug.exceptions import HTTPException


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
db = SQLAlchemy(app)
hashids = Hashids(app)


class User(HashidMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    @property
    def url(self):
        return url_for('read_user', user_id=self.id)

    def to_json(self):
        return {'id': self.hashid, 'name': self.name, 'url': self.url}


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(HTTPException)
def generic_error_handler(e):
    return jsonify(e.description), e.code


@app.route('/users', methods=['POST'])
def create_user():
    user = User(name=request.json['name'])
    db.session.add(user)
    db.session.commit()
    return user.to_json(), 201


@app.route('/users')
def read_users():
    users = [u.to_json() for u in User.query.all()]
    return users, 200


@app.route('/users/<hashid:user_id>')
def read_user(user_id):
    print(user_id)
    user = User.query.get_or_404(user_id)
    return user.to_json(), 200


@app.route('/users/<hashid:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    user.name = request.json.get('name', user.name)
    db.session.commit()
    return jsonify(''), 204, {'Content-Location': user.url}


@app.route('/users/<hashid:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify(''), 204


def main():
    app.run()


if __name__ == '__main__':
    main()
