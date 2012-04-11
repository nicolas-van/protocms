
import sqlalchemy
import os.path
import sqlalchemy.orm
import sqlalchemy.ext.declarative 
from sqlalchemy import Column, Integer, String, Sequence

filename = "database.sqlite"

engine = sqlalchemy.create_engine('sqlite:///' + filename, echo=True)

class Base(object):
    @sqlalchemy.ext.declarative.declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @sqlalchemy.ext.declarative.declared_attr
    def id(cls):
        return Column(Integer, Sequence(cls.__name__.lower() + "_id_seq"), primary_key=True)

Base = sqlalchemy.ext.declarative.declarative_base(cls=Base)

class Article(Base):
    content  = Column(String(1000))

Session = sqlalchemy.orm.sessionmaker(bind=engine)

if not os.path.exists(filename): 
    Base.metadata.create_all(engine) 
    session = Session()
    try:
        article = Article(content="dans la vallee!")
        session.add(article)
        session.commit()
    finally:
        session.close()

