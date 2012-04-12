
import sqlalchemy
import os.path
import sqlalchemy.orm
import sqlalchemy.ext.declarative 
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import relationship

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

def Many2One(class_name, **kwargs):
    return Column(Integer, sqlalchemy.ForeignKey(class_name.lower() + ".id"), **kwargs)

class ArticleType(Base):
    key = Column(String(30), index=True, unique=True, nullable=False)
    name = Column(String(50))

    @staticmethod
    def by_key(key):
        return Session().query(ArticleType).filter(ArticleType.key == key).one()

class Article(Base):
    content  = Column(String(1000))
    type_id = Many2One("ArticleType", nullable=False)

    type = relationship("ArticleType")
    

Session = sqlalchemy.orm.scoped_session(sqlalchemy.orm.sessionmaker(bind=engine))

def transactionnal(fct):
    def wrapping(*args, **kwargs):
        Session()
        try:
            val = fct(*args, **kwargs)
            Session().commit()
            return val
        finally:
            Session.remove()
    return wrapping

if not os.path.exists(filename): 
    Base.metadata.create_all(engine) 
    @transactionnal
    def create_data():
        Session().add_all([
            ArticleType(key="blog_post", name="Blog Post"),
            ArticleType(key="page", name="Page"),
        ])

        article = Article(content="Hello World", type=ArticleType.by_key("blog_post"))
        Session().add(article)

    create_data()

