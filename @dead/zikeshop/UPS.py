"""
UPS integration.. this is just a prototype, and will be spun
off into its own module...

http://www.ec.ups.com/ecommerce/techdocs/e5c9_ratesdata.html
"""

import urllib
import multifile
import mimetools
import string

def getRate(fromZip, toZip, toCountryCD, weight, isResidential=1, level="GND"):

    data = {
        "AppVersion":  "1.2",
        "AcceptUPSLicenseAgreement":  "yes",
        "ResponseType":  "application/x-ups-rss",
        "ActionCode":  "3", # show for selected service only
        "ServiceLevelCode":  level,
        "RateChart":  "Regular Daily Pickup",
        "ShipperPostalCode":  fromZip,
        "ConsigneePostalCode":  toZip,
        "ConsigneeCountry":  toCountryCD,
        "ResidentialInd":  isResidential,
        "PackagingType": "00", # shipper supplied packaging
        "PackageActualWeight": weight,
        "service":"Regular Daily Pickup",
        }



    page = multifile.MultiFile(urllib.urlopen(
        "http://www.ups.com/using/services/rave/qcost_dss.cgi",
        urllib.urlencode(data)), 0)

    page.push("UPSBOUNDARY")
    page.next()
    page.next()

    res = string.split(mimetools.Message(page, 0).fp.read(), "%")
    return res[-2]


if __name__=="__main__":
    assert getRate("30041", "90210", "US", 10, 1) == "8.34", \
           "unexpected rate. double check at ups.com"
    print "yay! it works!"
    
