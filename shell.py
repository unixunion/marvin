import cmd, sys
import libmarvin
import libmarvin.settingsloader as settings
import requests
import pprint

# curl -X POST localhost:5000/parse -d '{"q":"what capital city of france"}' | python -m json.tool
from libmarvin import util
from libmarvin.session import Session


class BotShell(cmd.Cmd):
    intro = 'Welcome to the interactive experience.\n'
    prompt = 'marvin> '

    session = Session()

    # def precmd(self, line):
    #     line = line.lower()
    #     return line
    def quit(self, line):
        sys.exit(0)

    def default(self, line):
        # line = line.lower()
        # try:
        print (self.session.query(line))
        # try:
        #     r = requests.post("http://localhost:5000/parse", data='{"q": "%s"}' % line)
        #     pprint.pprint (r.json())
        # except Exception as e:
        #     print (e)
        #     pass

if __name__ == '__main__':
    BotShell().cmdloop()