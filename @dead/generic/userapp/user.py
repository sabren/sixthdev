"""
authentication / signup process for linkwatcher
"""
__ver__="$Id$"
import weblib, zebra, zdc, zikebase,linkwatcher
zikebase.load("UserApp")

class LWUserApp(zikebase.UserApp):
    __super = zikebase.UserApp
    userClass = linkwatcher.LWUser

if __name__=="__main__":
    LWUserApp().act()
