"""
the lecter shell
"""
__ver__="$Id$"

import cmd, pprint, lecter, os, sys

class Shell(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "lectsh> "
        self.i = lecter.Interpreter()

    def do_quit(self, arg):
        sys.exit()

    def do_clear(self, arg):
        os.system("clear")

    def do_reset(self, arg):
        raise lecter.Reset

    def do_test(self, arg):
        os.system('zikeunit')

    def default(self,line):
        if line[0]=="!":
            if line[1:]:
                os.system(line[1:])
            else:
                os.system('cmd')
        else:
            try:
                res = self.i.eval(line)
                if res is not None:
                    pprint.pprint(res)
            except:
                import string, traceback
                print string.join(traceback.format_exception(
                    sys.exc_type,
                    sys.exc_value,
                    sys.exc_traceback), '')
                
