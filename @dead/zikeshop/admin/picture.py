"""
picture server for zikeshop!. This is the same on both public/admin sides.
"""
import zikeshop

import weblib, zikeshop
weblib.auth.check()
zikeshop.showPicture()
