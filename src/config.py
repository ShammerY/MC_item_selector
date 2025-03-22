# class Config:
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'items.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
