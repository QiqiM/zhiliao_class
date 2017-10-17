#encoding:utf-8
import os

DEBUG = True

SECRET_KEY = os.urandom(24)  #加密字符串
DIALECT = 'mysql'
DRIVER = 'mysqldb'
USERNAME = 'root'
PASSWORD = ''
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'ytt'

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,DRIVER,USERNAME,PASSWORD,
                         HOST,PORT,DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False