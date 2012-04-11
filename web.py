import db
import flask
app = flask.Flask(__name__)
app.debug = True

def route(*args, **kwargs):
    def wrapper(fct):
        return app.route(*args, **kwargs)(db.transactionnal(fct))
    return wrapper

@route("/")
def root():
    return flask.redirect(flask.url_for('index'))

@route("/index.html")
def index():
    articles = db.Session().query(db.Article).all()
    return flask.render_template('index.html', articles=articles)

