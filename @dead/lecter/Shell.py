"""
the lecter shell
"""
__ver__="$Id$"

import cmd, pprint, lecter

class Shell(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "lectsh> "
        self.i = lecter.Interpreter()

    def do_quit(self, arg):
        import sys
        sys.exit()

    def do_clear(self, arg):
        import os
        os.system("clear")

    def do_reset(self, arg):
        raise lecter.Reset

    def do_test(self, arg):
        import os
        os.system('zikeunit')

    def default(self,line):
        try:
            res = self.i.eval(line)
            if res is not None:
                pprint.pprint(res)
        except:
            import string, sys, traceback
            print string.join(traceback.format_exception(
                sys.exc_type,
                sys.exc_value,
                sys.exc_traceback), '')

