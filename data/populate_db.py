import sqlalchemy as db
from sqlalchemy import MetaData
from sqlalchemy import insert
import bcrypt
import os
import json
import datetime as dt

POSTGRES_URL = os.getenv('POSTGRES_URL')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')

engine = db.create_engine('postgres://{user}:{pwd}@{url}/{db}'.format(
    user=POSTGRES_USER,
    pwd=POSTGRES_PASSWORD,
    url=POSTGRES_URL,
    db=POSTGRES_DB
))

metadata = MetaData()
metadata.reflect(bind=engine)

connection = engine.connect()


def main():
    # create users
    with open('users.json') as f:
        users_json = json.load(f)

    for i, user in enumerate(users_json['users']):
        print(f'user {i}: {user}')

        password = str(user['password']).encode('utf-8')
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        query = insert(metadata.tables['users']).values(
            id=i,
            username=user['username'],
            email=user['email'],
            password=hashed_password,
            created_on=dt.datetime.utcnow(),
            last_login=dt.datetime.utcnow(),
            avatar_url=user['avatar_url']
        )

        connection.execute(query)

    # create songs
    with open('songs.json') as f:
        songs_json = json.load(f)

    for i, song in enumerate(songs_json['songs']):
        print(f'song {i}: {song}')

        query = insert(metadata.tables['songs']).values(
            id=i,
            title=song['title'],
            artist=song['artist'],
            album=song['album'],
            created_on=dt.datetime.utcnow(),
            cover_url=song['cover_url']
        )

        connection.execute(query)

    # create user songs
    with open('user_songs.json') as f:
        usersongs_json = json.load(f)

    for i, user_song in enumerate(usersongs_json['user_songs']):
        print(f'user song {i}: {user_song}')

        query = insert(metadata.tables['user_songs']).values(
            id=i,
            user_id=user_song['user_id'],
            song_id=user_song['song_id']
        )

        connection.execute(query)


if __name__ == '__main__':
    main()
