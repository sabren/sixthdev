"""
A class to coordinate the a Parser and a Generator.

$Id$
"""

from zebra import Parser, Generator

class Engine:

    def __init__(self, generator=None):
        self.parser = Parser()
        if generator == None:
            self.generator = Generator()
        else:
            self.generator = generator

    def parse(self, text):
        return self.parser.parse(text)
            
    def compile(self, text):
        return self.generator.generate(self.parse(text))

