@echo off
REM = """ 
REM python -x skips first line of source..

REM make sure to change the next line to 
REM whatever this file is called:

call python -x test.bat
goto end
"""

from weblib import test
test.run()

"""
:end """
