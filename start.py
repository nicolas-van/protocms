import web
import sys

commands = {}

def start():
    web.app.run()
commands["start"] = start

def generate():
    pass
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
