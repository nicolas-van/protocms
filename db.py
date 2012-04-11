
import sqlalchemy
import os.path
import sqlalchemy.orm
import sqlalchemy.ext.declarative 
from sqlalchemy import Column, Integer, String, Sequence

filename = "database.sqlite"

engine = sqlalchemy.create_engine('sqlite:///' + filename, echo=True)

Base = sqlalchemy.ext.declarative.declarative_base()

class User(Base):
     __tablename__ = 'users'

     id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
     name = Column(String)
     fullname = Column(String)
     password = Column(String)
     brole = Column(String)

     def __init__(self, name, fullname, password):
         self.name = name
         self.fullname = fullname
         self.password = password

     def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.name, self.fullname, self.password)

Session = sqlalchemy.orm.sessionmaker(bind=engine)

if not os.path.exists(filename): 
    Base.metadata.create_all(engine) 
    session = Session()
    try:
        user = User("fred", "vargas", "yop")
        session.add(user)
        session.commit()
    finally:
        session.close()
