import unittest
import seismq
import sqlite
import os

class MQTest(unittest.TestCase):
   
    def setUp(self):
        filename = "test/test.mq"
        if os.path.exists(filename):
            os.unlink(filename)
        self.smq = seismq.open(filename)
        self.sql = sqlite.connect(filename)

    def test_open(self):
        assert self.smq.hasTable()

    def test_send(self):
        self.smq.send("message")
        assert self.smq.count("message") == 1
        self.smq.send("message")
        assert self.smq.count("message") == 2


    def test_take(self):
        assert self.smq.count("message") == 0
        self.smq.send("message")
        assert self.smq.count("message") == 1
        taken = self.smq.take("message")
        assert taken == ["message"]
        assert self.smq.count("message") == 0

    def test_close(self):
        self.smq.close()
        assert self.smq.dbc.closed

      

if __name__=="__main__":
    unittest.main()
