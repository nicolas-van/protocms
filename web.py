import db
import flask
app = flask.Flask(__name__)
app.debug = True

def route(*args, **kwargs):
    def wrapper(fct):
        @app.route(*args, **kwargs)
        @db.transactionnal
        def wrapper2(*args2, **kwargs2):
            return fct(*args2, **kwargs2)
        return wrapper2
    return wrapper

@route("/")
def root():
    return flask.redirect(flask.url_for('index'))

@route("/index.html")
def index():
    articles = db.Session().query(db.Article).all()
    return flask.render_template('index.html', articles=articles)

