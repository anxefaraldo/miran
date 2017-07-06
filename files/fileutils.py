#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

"""
Function definitions for file and directory easy handeling."

Ángel Faraldo, March 2015.
"""

import os

def listfiles(d):
    l = os.listdir(d)
    if '.DS_Store' in l:
	    l.remove('.DS_Store')
    return l    
