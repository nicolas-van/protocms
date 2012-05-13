
import orpheus.db as db
import flask
import os
import os.path

import config

app = flask.Flask(__name__)
app.template_folder = os.path.abspath(config.template_folder)
app.static_folder = os.path.abspath(config.static_folder)
app.debug = True

static_pages_fcts = []

def gen_static_files_urls():
    files = []
    def find_files(folder, url):
        for f in os.listdir(folder):
            if os.path.isdir(os.path.join(folder, f)):
                find_files(os.path.join(folder, f), os.path.join(url, f))
            else:
                files.append(os.path.join(url, f))
    find_files(app.static_folder, "/static")
    return files
static_pages_fcts.append(gen_static_files_urls)

def route(*args, **kwargs):
    def wrapper(fct):
        tmp = dict(kwargs)
        tmp.setdefault("endpoint", fct.__name__)
        tmp["view_func"] = db.transactionnal(fct)
        app.add_url_rule(*args, **tmp)
        return fct
    return wrapper


