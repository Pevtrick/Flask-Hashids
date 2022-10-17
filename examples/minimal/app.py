from flask import Flask, jsonify, url_for
from flask_hashids import HashidMixin, Hashids
from flask_sqlalchemy import SQLAlchemy


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
        return url_for('user', user_id=self.id)

    def to_json(self):
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
    return [user.to_json() for user in User.query.all()], 200


@app.route('/users/<hashid:user_id>')
def user(user_id: int):
    user = User.query.get(user_id)
    if user is None:
        return jsonify('User not found'), 404
    return user.to_json(), 200


def main():
    app.run()


if __name__ == '__main__':
    main()
