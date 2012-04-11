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
        users = session.query(db.User).filter(db.User.name.in_(["fred"])).all()
        print users
        return flask.render_template('index.html', user=users[0])
    finally:
        session.close()


