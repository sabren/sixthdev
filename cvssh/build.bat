REM  cvsssh compilation batchfile
call python20 setup.py py2exe
call python20 setup_stub.py py2exe
copy dist\stub\* .
copy dist\cvssh\* .
