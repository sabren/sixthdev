pass

#@TODO: put these into a test case
if 0:
    def check_dateRange(self):
        range = zdc.dateRange("1/1/2001", "1/10/2001")
        assert len(range) == len([1,2,3,4,5,6,7,8,9,10]), "wrong length"


    def check_toDate(self):
        assert isinstance(zdc.toDate("1/1/2001"), zdc.Date)
        assert isinstance(zdc.toDate(zdc.toDate("1/1/2001")), zdc.Date)
