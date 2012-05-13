
import sqlalchemy
import os.path
import sqlalchemy.orm
import sqlalchemy.ext.declarative 
from sqlalchemy import Column, Integer, String, Sequence, Boolean
from sqlalchemy.orm import relationship
import threading

import config

DEBUG = False

engine = sqlalchemy.create_engine(config.db_connection_string, echo=DEBUG)

# Some helpers to help use SqlAlchemy
class Base(object):
    @sqlalchemy.ext.declarative.declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @sqlalchemy.ext.declarative.declared_attr
    def id(cls):
        return Column(Integer, Sequence(cls.__name__.lower() + "_id_seq"), primary_key=True)

Base = sqlalchemy.ext.declarative.declarative_base(cls=Base)

def Many2One(class_name, **kwargs):
    return Column(Integer, sqlalchemy.ForeignKey(class_name.lower() + ".id"), **kwargs)

class ThreadSession:
    def __init__(self, session_class):
        self._session_class = sqlalchemy.orm.scoped_session(session_class)
    def __getattr__(self, name):
        return getattr(self._session_class(), name)
    def ensure_inited(self):
        return self._session_class()
    def remove(self):
        return self._session_class.remove()

# models

class Article(Base):
    name = Column(String(50), nullable=False)
    content  = Column(String(1000), default="Yop", nullable=False)
    published = Column(Boolean(), default=False, nullable=False)


# session

session = ThreadSession(sqlalchemy.orm.sessionmaker(bind=engine))

_local_test = threading.local()

def transactionnal(fct):
    def wrapping(*args, **kwargs):
        if getattr(_local_test, "test", 0) != 0:
            raise Exception("Multiple usages of @transactionnal")
        _local_test.test = 1
        session.ensure_inited()
        try:
            val = fct(*args, **kwargs)
            session.commit()
            return val
        finally:
            _local_test.test = 0
            session.remove()
    return wrapping

# database initialisation

def init_db():
    if len(Base.metadata.tables.keys()) == 0:
        return
    tname = Base.metadata.tables.keys()[0]
    if not engine.dialect.has_table(engine, tname):
        Base.metadata.create_all(engine) 
        @transactionnal
        def create_data():
            for i in range(17):
                article = Article(name="Something %d" % i, content="Hello world %d!" % i, published=True)
                session.add(article)

        create_data()

def drop_db():
    Base.metadata.drop_all(engine)

