# type: function
# api: python
# title: help pages
# description: invokes yelp/mallard browser
# version: 0.1
#
# No pages to speak of yet.
#


import os, re

__dir__ = re.sub("[\w.-]+$", "", __file__)

def help():
    os.system(f"yelp %r &" % __dir__)
