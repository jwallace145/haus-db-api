from database import db
from sqlalchemy_serializer import SerializerMixin
import datetime as dt


class Song(db.Model, SerializerMixin):
    __tablename__ = 'songs'

    serialize_only = (
        'id',
        'title',
        'artist',
        'album',
        'created_on',
        'cover_url'
    )

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    artist = db.Column(db.String(50), nullable=False)
    album = db.Column(db.String(50), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    cover_url = db.Column(db.String(
        100), default='https: // jwalls-fun-bucket.s3.amazonaws.com/album-covers/default-cover.jpg', nullable=False)

    def __init__(self, title, artist, album) -> None:
        self.title = title
        self.artist = artist
        self.album = album
        self.created_on = dt.datetime.utcnow()

    def __repr__(self) -> str:
        return super().__repr__()
