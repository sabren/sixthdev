"""
code to convert xml to a model usable by zebra reports.
"""
__ver__="$Id$"
import xmllib

class X2M(xmllib.XMLParser):
    "I parse XML into zebra-style models."

    def translate(self, xml):
        "X2M().translate(xml) => a model of the xml data."
        self.reset()
        self.feed(xml)
        return self.model

    def reset(self):
        "Overrides XMLParser to also initialize the model."
        xmllib.XMLParser.reset(self)
        self.model = []
        self.model_point = self.model
        self.point_stack = self.model
        
    def unknown_starttag(self, tag, attributes):
        "Add a dict describing the tag to the model, then add it to stack."
        dict = {"__tag__": tag, "__data__":[]}
        dict.update(attributes)

        self.model_point.append(dict)
        self.point_stack.append(self.model_point)
        self.model_point=dict["__data__"]

    def unknown_endtag(self, tag):
        "Pop the point off the point stack."
        self.model_point = self.point_stack.pop()

    def handle_data(self, data):
        self.model_point.append(data)
        
