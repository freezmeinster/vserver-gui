from lib.sqlalchemy import Table, Column, String, Integer, MetaData, ForeignKey
from lib.sqlalchemy.orm import mapper

metadata = MetaData()

users = Table('users', metadata,
        Column('id', Integer, primary_key=True),
        Column('username', String),
        Column('password', String),
        Column('name', String)
    )

class User(object):
    def __init__(self,username,password,name):
        self.username = username
        self.password = password
        self.name = name
        
    def __repr__(self):
        return "%s" % self.name
        

mapper(User, users)