
import sqlalchemy
import os.path
import sqlalchemy.orm
import sqlalchemy.ext.declarative 
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import relationship
import threading

filename = "database.sqlite"

DEBUG = False

engine = sqlalchemy.create_engine('sqlite:///' + filename, echo=DEBUG)

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

class ArticleType(Base):
    key = Column(String(30), index=True, unique=True, nullable=False)
    name = Column(String(50))

    @staticmethod
    def by_key(key):
        return session.query(ArticleType).filter(ArticleType.key == key).one()

class Article(Base):
    content  = Column(String(1000), default="Yop")
    type_id = Many2One("ArticleType", nullable=False)

    type = relationship("ArticleType")

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

if not os.path.exists(filename): 
    Base.metadata.create_all(engine) 
    @transactionnal
    def create_data():
        session.add_all([
            ArticleType(key="blog_post", name="Blog Post"),
            ArticleType(key="page", name="Page"),
        ])
        for i in range(17):
            article = Article(type=ArticleType.by_key("blog_post"))
            session.add(article)

    create_data()

