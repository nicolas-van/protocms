import web
import db
import sys
import threading
import httplib

commands = {}

def start():
    web.app.run()
commands["start"] = start

def generate():
    @db.transactionnal
    def generate_urls():
        urls = []
        for fct in web.static_pages_fcts:
            print urls
            urls = urls + fct()
        return urls
    urls = generate_urls()

    def run_app():
        web.app.run()
    thread = threading.Thread(target=run_app)
    thread.start()
    conn = httplib.HTTPConnection("localhost:5000")
    res = conn.request("GET", "/index.html")
    print res
commands["generate"] = generate

if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) >= 2 else ""
    if not command in commands:
        print "Invalid command, use one of these commands:"
        print ""
        for k in commands.keys():
            print k
        exit(-1)
    commands[command]()
