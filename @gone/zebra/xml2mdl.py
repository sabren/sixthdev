"""
routines to convert xml to a model usable by zebra reports.
"""
import xmllib

#####[ PARSER CLASS ]############################################

class X2mParser(xmllib.XMLParser):
    """A class to parse XML into zebra models."""

    ## setup ########################################

    def reset(self):
        """Overrides XMLParser to also initialize the model."""
        xmllib.XMLParser.reset(self)
        self.model = []
        self.model_point = self.model
        self.point_stack = self.model

    ## tag handlers #################################
        
    def unknown_starttag(self, tag, attributes):
        """Add a dict describing the tag to the model, then add it to stack."""

        dict = {"__tag__": tag, "__data__":[]}
        dict.update(attributes)

        self.model_point.append(dict)
        self.point_stack.append(self.model_point)
        self.model_point=dict["__data__"]


    def unknown_endtag(self, tag):
        """Pop the point off the point stack."""
        self.model_point = self.point_stack.pop()
        


    def handle_data(self, data):
        """Record data in the model."""
        import string
        if string.strip(data):
            self.model_point.append(data)
        

#####[ UTILITY FUNCTIONS ]#######################################

def xml2mdl(fp):
    """Reads from an XML file pointer and converts to a model."""
    pass


def xml2mdl_s(s):
    """Converts an XML string to a model."""
    pass

#####[ MAIN ]####################################################

if __name__=="__main__":
    #@TODO: import pprint, etc..
    pass
