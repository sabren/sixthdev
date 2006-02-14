import re, sys


e = re.compile(r"(\d{4}/\d{2}/\d{2})(.*){(\d{4}/\d{2}/\d{2})}")

for line in sys.stdin:
    sys.stdout.write(e.sub(r"\3\2",line))
    
