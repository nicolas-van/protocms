import db
import web
import flask
import os
import os.path
from flask import json
import logging
from sqlalchemy import sql

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
                "code": -32000,
                "message": unicode(e),
                "data": {
                    "traceback": traceback.format_exc(),
                },
            },
            "id": data["id"],
        })

@web.route("/admin/<path:file_>")
def admin_static(file_):
    path = os.path.join(os.path.dirname(__file__), "adminstatic", file_)
    return flask.send_file(path)

@rpc
def search_count(table_name, columns=None, offset=None, limit=None, order_by=None):
    table = db.Base.metadata.tables[table_name]
    to_select = None
    if columns is None:
        to_select = [table]
    else:
        to_select = [table.columns[x] for x in columns]
    q = sql.select(to_select)
    count = db.session.execute(q.count()).fetchone()[0]
    
    if offset is not None:
        q = q.offset(offset)
    if limit is not None:
        q = q.limit(limit)
    if order_by is not None:
        col = table.columns[order_by]
        q = q.order_by(col)
    result = db.session.execute(q)
    return {
        "count": count,
        "list": [dict(x) for x in result],
    }


