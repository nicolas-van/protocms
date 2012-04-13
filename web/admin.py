import db
import web
import flask
import os
import os.path

@web.route("/admin")
def admin():
    return flask.redirect("/admin/index.html")

@web.route("/admin/<path:file_>")
def admin_static(file_):
    path = os.path.join(os.path.dirname(__file__), "adminstatic", file_)
    return flask.send_file(path)

