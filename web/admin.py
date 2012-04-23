import db
import web
import flask
import os
import os.path
from flask import json
import logging

_logger = logging.getLogger(__name__)

@web.route("/admin")
def admin():
    return flask.redirect("/admin/index.html")

rpc_methods = {}

def rpc(fct):
    rpc_methods[fct.__name__] = fct
    return fct

@web.route("/adminapi", methods=["POST"])
def admin_api():
    data = flask.request.json
    fct = rpc_methods[data["method"]]
    params = data["params"]
    try:
        res = fct(*params.get("args", []), **params.get("kwargs", {}))
        return flask.jsonify(**{
            "jsonrpc": "2.0",
            "result": res,
            "id": data["id"],
        })
    except Exception as e:
        import traceback
        _logger.error(traceback.format_exc())
        return flask.jsonify(**{
            "jsonrpc": "2.0",
            "error": {
                "traceback": traceback.format_exc(),
                "message": unicode(e)
            },
            "id": data["id"],
        })

@web.route("/admin/<path:file_>")
def admin_static(file_):
    path = os.path.join(os.path.dirname(__file__), "adminstatic", file_)
    return flask.send_file(path)

@rpc
def query_articles(limit):
    q = db.session.query(db.Article)
    count = q.count()
    result = db.session.execute(q.limit(limit))
    import pprint
    pprint.pprint(result)
    return {
        "count": count,
        "list": [dict(x) for x in result],
    }


