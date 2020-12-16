from database import db

UserSongs = db.Table('user_songs',
                     db.Column('id', db.Integer, primary_key=True),
                     db.Column('user_id', db.Integer, db.ForeignKey(
                         'users.id', ondelete='cascade')),
                     db.Column('song_id', db.Integer, db.ForeignKey(
                         'songs.id', ondelete='cascade'))
                     )
