from flask import Blueprint, request
from models.user.user import User
import bcrypt
from database import db
from clients import s3_client
from werkzeug.utils import secure_filename
import os

auth_blueprint = Blueprint('auth_blueprint', __name__)


@auth_blueprint.route('/login', methods=['POST'])
def login_user():
    username = request.form.get('username')
    password = bytes(request.form.get('password'), 'utf-8')

    user = db.session.query(User).filter_by(username=username).first()

    authenticate = bcrypt.checkpw(password, user.password)

    if authenticate:
        user.authenticated = True
        db.session.commit()

    return {
        'authenticated': authenticate,
        'user': user.to_dict()
    }


@auth_blueprint.route('/logout', methods=['POST'])
def logout_user():
    username = request.form.get('username')

    user = db.session.query(User).filter_by(username=username).first()

    user.authenticated = False

    db.session.commit()

    return {'user': user.to_dict()}


@auth_blueprint.route('/register', methods=['POST'])
def register_user():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    avatar = request.files['avatar']

    hashed_password = bcrypt.hashpw(
        str(password).encode('utf-8'), bcrypt.gensalt())

    user = User(
        username=username,
        email=email,
        password=hashed_password
    )

    filename = secure_filename(avatar.filename)
    avatar.save(filename)

    s3_client.upload_file(
        Bucket='jwalls-fun-bucket',
        Filename=filename,
        Key=f'profile-pics/{filename}',
        ExtraArgs={'ACL': 'public-read'}
    )

    os.remove(filename)

    user.avatar_url = f'https://jwalls-fun-bucket.s3.amazonaws.com/profile-pics/{filename}'

    db.session.add(user)
    db.session.commit()

    user = db.session.query(User).filter_by(username=username).first()

    return {'user': user.to_dict()}
