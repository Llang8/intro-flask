from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime as dt

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    posts= db.relationship('Post', backref='user')

    def generate_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

@login_manager.user_loader
def get_user(user_id):
    return User.query.get(int(user_id))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=dt.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        data = {
            'body': self.body,
            'date_created': self.date_created,
            'user': User.query.get(self.user_id).to_dict()
        }
        # data['user'].extend()
        return data