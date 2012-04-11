import db
import flask
app = flask.Flask(__name__)
app.debug = True

@app.route("/")
def root():
    return flask.redirect(flask.url_for('index'))

@app.route("/index.html")
def index():
    session = db.Session()
    try:
        articles = session.query(db.Article).all()
        print articles
        return flask.render_template('index.html', articles=articles)
    finally:
        session.close()


