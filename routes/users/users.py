import bcrypt
from database import db
from flask import Blueprint, request
from models.user.user import User
from clients import s3_client
from werkzeug.utils import secure_filename
import os

users_blueprint = Blueprint('users_blueprint', __name__)


@users_blueprint.route('/edit', methods=['PUT'])
def edit_user():
    """
    Edit user.
    """

    user_id = request.args.get('user_id')
    username = request.args.get('username')

    user = None
    if user_id:
        user = db.session.query(User).get(user_id)
    elif username:
        user = db.session.query(User).filter_by(username=username).first()

    new_username = request.form.get('username')
    new_email = request.form.get('email')
    new_avatar = request.files['avatar']

    filename = secure_filename(new_avatar.filename)
    new_avatar.save(filename)

    s3_client.upload_file(
        Bucket='jwalls-fun-bucket',
        Filename=filename,
        Key=f'profile-pics/{filename}',
        ExtraArgs={'ACL': 'public-read'}
    )

    os.remove(filename)

    user.username = new_username
    user.email = new_email
    user.avatar_url = f'https://jwalls-fun-bucket.s3.amazonaws.com/profile-pics/{filename}'

    db.session.commit()

    user = db.session.query(User).filter_by(username=new_username).first()

    return {'user': user.to_dict()}


@users_blueprint.route('/get', methods=['GET'])
def get_user():
    """
    Get user by user id or username.

    Args:
        user_id (request.args): The user id to query.
        username (request.args): The username to query.

    Returns:
        result (dict): {
            'exists': (bool) if user exists,
            'user': {
                'id': (int) user id,
                'username': (str) user username,
                'email': (str) user email,
                'authenticated': (bool) user authenticated,
                'last_login': (datetime) user last login,
                'created_on': (datetime) user created on
            }
        }
    """

    user_id = request.args.get('user_id')
    username = request.args.get('username')

    user = None
    if user_id:
        user = db.session.query(User).get(user_id)
    elif username:
        user = db.session.query(User).filter_by(username=username).first()

    return {
        'exists': True if user else False,
        'user': user.to_dict() if user else {}
    }


@users_blueprint.route('/all', methods=['GET'])
def get_all_users():
    """
    Get all users.

    Returns:
        (dict): {
            'count': (int) number of users,
            'users': {
                'id': (int) user id,
                'username': (str) user username,
                'email': (str) user email,
                'authenticated': (bool) user authenticated,
                'last_login': (datetime) user last login,
                'created_on': (datetime) user created on
            }
        }
    """

    users = db.session.query(User).all()

    return {
        'count': len(users),
        'users': [user.to_dict() for user in users]
    }


@users_blueprint.route('/create', methods=['POST'])
def create_user():
    """
    Create new user.

    Args:
        username (request.json): The username of the new user.
        email (request.json): The email of the new user.
        password (request.json): The password of the new user.

    Returns:
        (dict): {
            'created': (bool) created,
            'user': {
                'id': (int) user id,
                'username': (str) user username,
                'email': (str) user email,
                'authenticated': (bool) user authenticated,
                'last_login': (datetime) user last login,
                'created_on': (datetime) user created on
            }
        }
    """

    # encode the password and hash
    password = str(request.get_json()['password']).encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

    user = User(
        username=request.get_json()['username'],
        password=hashed_password,
        email=request.get_json()['email']
    )

    db.session.add(user)
    db.session.commit()

    user = db.session.query(User).get(user.id)

    return {'user': user.to_dict()}


@users_blueprint.route('/delete-all', methods=['DELETE'])
def delete_all_users():
    users = db.session.query(User).all()
    deleted_users = [db.session.delete(user) for user in users]
    db.session.commit()

    return {'numberOfDeletedUsers': len(deleted_users)}
