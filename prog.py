import web
import db
import sys
import os.path
import os
import logging

commands = {}

web.app.template_folder = os.path.abspath("templates")
web.app.static_folder = os.path.abspath("static")

def start():
    web.app.run()
commands["start"] = start

FOLDER = "dist"

def generate():
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
            path = os.path.join(FOLDER, path)
            if not os.path.exists(os.path.dirname(path)):
                os.makedirs(os.path.dirname(path))
            with open(path, "w") as f:
                if type(x) == str or type(x) == unicode:
                    f.write(x)
                else:
                    f.write(x.data)

commands["generate"] = generate

if __name__ == "__main__":
    logging.basicConfig()
    command = sys.argv[1] if len(sys.argv) >= 2 else ""
    if not command in commands:
        print "Invalid command, use one of these commands:"
        print ""
        for k in commands.keys():
            print k
        exit(-1)
    commands[command]()

