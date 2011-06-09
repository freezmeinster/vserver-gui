import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_name = 'vserver-gui.db'
db_path = os.path.join(os.path.dirname(__file__),'db_store')
engine = create_engine("sqlite:///"+db_path+"/"+db_name+"", echo=True)
Session = sessionmaker(bind=engine)
session = Session()
