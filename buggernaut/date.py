"""
date conversion routines for use with MySQL..
"""
__ver__="$Id$"

def sql2us(value):
    if not value:
        return None
    else:
        import string
        y,m,d = map(int,string.split(value[:10],"-"))
        return "%02i/%02i/%04i" % (m,d,y)

def us2sql(value):
    # 2001-03-12 01:00:00 is mysql, but we want 03/12/2001
    if not value:
        return None
    else:
        import string
        m,d,y = map(int, string.split(value, "/"))
        return "%04i-%02i-%02i" % (y,m,d)

    
if __name__=="__main__":
    assert us2sql("3/12/2001")=="2001-03-12", "wrong: %s" % us2sql("3/12/2001")
    assert sql2us("2001-03-12")=="03/12/2001", "wrong: %s" % sql2us("2001-03-12")

