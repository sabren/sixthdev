"""
lecter shell
"""
__ver__="$Id$"
import cmd
import lecter
import pprint

class Restart(Exception):
    pass

class lecterCMD(cmd.Cmd):
    def __init__(self):
        self.prompt = "lectsh> "
        self.i = lecter.Interpreter()

    def do_quit(self, arg):
        import sys
        sys.exit()

    def do_clear(self, arg):
        import os
        os.system("cls")

    def do_restart(self, arg):
        print "restarting..."

    def do_reset(self, arg):
        reload(lecter)
        self.i = lecter.Interpreter()
        print "environment reset."

    def do_test(self, arg):
        import os
        os.system('zikeunit')

    def default(self,line):
        try:
            pprint.pprint(self.i.eval(line))
        except:
            import string, sys, traceback
            print string.join(traceback.format_exception(
                sys.exc_type,
                sys.exc_value,
                sys.exc_traceback), '')


while 1:
    try:
        lecterCMD().cmdloop()
    except Restart:
        continue
