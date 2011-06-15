import datetime
from lib.sqlalchemy import Table, Column, String, Integer, DateTime, MetaData, ForeignKey
from lib.sqlalchemy.orm import mapper

metadata = MetaData()

vservers = Table('vserver', metadata,
               Column('id', Integer, primary_key=True),
               Column('name', String),
               Column('ip', String),
               Column('password', String),
               Column('memory', Integer),
               Column('create_date', DateTime)
       )

class Vserver(object):
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.ip = kwargs['ip']
        self.password = kwargs['password']
        self.memory = kwargs['memory']
        self.create_date = datetime.datetime.now()
        
    def __repr__(self):
        return "%s di ip %s" %(self.name,self.ip)
        
        
mapper(Vserver, vservers)