from flask import Blueprint, request
from database import db
from models.song.song import Song
from models.user.user import User
from models.usersong.usersong import UserSongs
from werkzeug.utils import secure_filename
from clients import s3_client
from sqlalchemy import func
import os

songs_blueprint = Blueprint('songs_blueprint', __name__)


@songs_blueprint.route('/liked-by', methods=['GET'])
def get_liked_songs_by_user():
    user_id = request.args.get('user_id')
    username = request.args.get('username')

    user = None
    if user_id:
        user = db.session.query(User).get(user_id)
    elif username:
        user = db.session.query(User).filter_by(username=username).first()

    songs = db.session.query(
        Song.id,
        Song.title,
        Song.artist,
        Song.album,
        Song.created_on,
        Song.cover_url,
        func.count(UserSongs.c.song_id)
    ).filter(
        Song.id == UserSongs.c.song_id,
        UserSongs.c.user_id == user.id
    ).group_by(
        Song.id
    ).order_by(
        func.count(UserSongs.c.song_id).desc()
    )

    results = []
    for song in songs:
        results.append({
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'album': song.album,
            'created_on': song.created_on,
            'cover_url': song.cover_url,
            'likes': song[6]
        })

    return {
        'user_id': user.id,
        'username': user.username,
        'count': songs.count(),
        'songs': results
    }


@songs_blueprint.route('/liked', methods=['GET'])
def get_liked_songs():
    """
    Get most liked songs in descending order.

    Args:

    """
    songs = db.session.query(
        Song.id,
        Song.title,
        Song.artist,
        Song.album,
        Song.created_on,
        Song.cover_url,
        func.count(UserSongs.c.song_id)
    ).filter(
        Song.id == UserSongs.c.song_id
    ).group_by(
        Song.id
    ).order_by(
        func.count(UserSongs.c.song_id).desc()
    )

    results = []
    for song in songs:
        results.append({
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'album': song.album,
            'created_on': song.created_on,
            'cover_url': song.cover_url,
            'likes': song[6]
        })

    return {
        'count': songs.count(),
        'songs': results
    }


@songs_blueprint.route('/recent', methods=['GET'])
def get_recent_songs():
    songs = db.session.query(
        Song.id,
        Song.title,
        Song.artist,
        Song.album,
        Song.created_on,
        Song.cover_url,
        func.count(UserSongs.c.song_id)
    ).filter(
        Song.id == UserSongs.c.song_id
    ).group_by(
        Song.id
    ).order_by(
        Song.created_on.desc()
    )

    results = []
    for song in songs:
        results.append({
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'album': song.album,
            'created_on': song.created_on,
            'cover_url': song.cover_url,
            'likes': song[6]
        })

    return {
        'count': songs.count(),
        'songs': results
    }


@songs_blueprint.route('/create', methods=['POST'])
def create_song():
    """
    Create a new song
    """

    user_id = request.args.get('user_id')
    username = request.args.get('username')
    title = request.form.get('title')
    artist = request.form.get('artist')
    album = request.form.get('album')
    cover = request.files['cover']

    song = Song(
        title=title,
        artist=artist,
        album=album
    )

    user = None
    if user_id:
        user = db.session.query(User).get(user_id)
    elif username:
        user = db.session.query(User).filter_by(username=username).first()

    filename = secure_filename(cover.filename)
    cover.save(filename)

    s3_client.upload_file(
        Bucket='jwalls-fun-bucket',
        Filename=filename,
        Key=f'album-covers/{filename}',
        ExtraArgs={'ACL': 'public-read'}
    )

    os.remove(filename)

    song.cover_url = f'https://jwalls-fun-bucket.s3.amazonaws.com/album-covers/{filename}'
    user.songs.append(song)
    db.session.commit()

    return {'successful': True}
