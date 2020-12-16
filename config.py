
import os

POSTGRES_URL = os.getenv('POSTGRES_URL')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')


class Config:
    DEBUG = True
    TESTING = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = 'postgres://{user}:{pwd}@{url}/{db}'.format(
        user=POSTGRES_USER,
        pwd=POSTGRES_PASSWORD,
        url=POSTGRES_URL,
        db=POSTGRES_DB
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'lasdjflkasdj'
