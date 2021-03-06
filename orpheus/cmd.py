import orpheus.web as web
import orpheus.db as db
import sys
import os.path
import os

import config

commands = {}

def start():
    db.init_db()
    web.app.run(port=config.port)
commands["start"] = start

def generate():
    db.init_db()
    @db.transactionnal
    def generate_urls():
        urls = []
        for fct in web.static_pages_fcts:
            urls = urls + fct()
        return urls
    urls = generate_urls()

    print urls
    print "Generation of the static content"
    for url in urls:
        with web.app.test_request_context(url, method="GET"):
            print "Generating", url
            x = web.app.dispatch_request()
            path = []
            parent = url
            while parent != '/':
                tmp = os.path.split(parent)
                path.insert(0, tmp[1])
                parent = tmp[0]
            path = os.path.join(*path)
            path = os.path.join(config.dist_folder, path)
            if not os.path.exists(os.path.dirname(path)):
                os.makedirs(os.path.dirname(path))
            with open(path, "w") as f:
                if type(x) == str or type(x) == unicode:
                    f.write(x)
                else:
                    f.write(x.data)

commands["generate"] = generate

def start():
    command = sys.argv[1] if len(sys.argv) >= 2 else ""
    if not command in commands:
        print "Invalid command, use one of these commands:"
        print ""
        for k in commands.keys():
            print k
        exit(-1)
    commands[command]()

