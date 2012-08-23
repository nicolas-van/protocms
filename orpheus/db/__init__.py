
import sqlalchemy as sa
from pyphilo import *
import pyphilo
import os.path

import config

DEBUG = False

engine.init_global_engine(config.db_connection_string, echo=DEBUG)

class Article(Base):
    name = sa.Column(sa.String(50), nullable=False)
    content  = sa.Column(sa.String(1000), default="Yop", nullable=False)
    published = sa.Column(sa.Boolean(), default=False, nullable=False)

def init_db():
    if pyphilo.init_db():
        @transactionnal
        def create_data():
            for i in range(17):
                article = Article(name="Something %d" % i, content="Hello world %d!" % i, published=True)
                session.add(article)

        create_data()

