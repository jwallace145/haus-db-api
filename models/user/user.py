import datetime as dt

from database import db
from models.usersong.usersong import UserSongs
from sqlalchemy.orm import backref
from sqlalchemy_serializer import SerializerMixin


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_only = (
        'id',
        'username',
        'email',
        'created_on',
        'last_login',
        'authenticated',
        'avatar_url'
    )

    serialize_rules = ('-password', '-songs')

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.Binary, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    last_login = db.Column(db.DateTime, nullable=False)
    authenticated = db.Column(db.Boolean, default=False, nullable=False)
    avatar_url = db.Column(db.String(
        100), default='https://jwalls-fun-bucket.s3.amazonaws.com/profile-pics/default-profile-pic.jpg', nullable=False)
    songs = db.relationship('Song', secondary=UserSongs,
                            backref='users', cascade='all,delete')

    def __init__(self, username, password, email) -> None:
        self.username = username
        self.password = password
        self.email = email
        self.created_on = dt.datetime.utcnow()
        self.last_login = dt.datetime.utcnow()

    def __repr__(self) -> str:
        return 'hello'
