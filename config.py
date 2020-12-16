
import os


class Config:
    DEBUG = True
    TESTING = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = 'postgres://{user}:{pwd}@{url}/{db}'.format(
        user=os.getenv('POSTGRES_USER'),
        pwd=os.getenv('POSTGRES_PASSWORD'),
        url=os.getenv('POSTGRES_URL'),
        db=os.getenv('POSTGRES_DB')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
