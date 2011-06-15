from lib.sqlalchemy import Table, Column, String, Integer, Text, MetaData, ForeignKey
from lib.sqlalchemy.orm import mapper

metadata = MetaData()

events = Table('event', metadata,
            Column('id', Integer, primary_key=True),
            Column('event_name', String),
            Column('description', Text),
            Column('code', Integer),
            sqlite_autoincrement=True
    )

class Event(object):
    def __init__(self, **kwargs)
        self.event_name = kwargs['event_name']
        self.description = kwargs['description']
        self.code = kwargs['code']
        
    def __repr__(self):
        return self.event_name
        

mapper(Event, events)