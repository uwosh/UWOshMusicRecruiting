# -*- coding: utf-8 -*-
#
# File: testVisit.py
#
# Copyright (c) 2008 by []
# Generator: ArchGenXML Version 2.0-beta10
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

##code-section module-header #fill in your manual code here
##/code-section module-header

#
# Test-cases for class(es) 
#

from Testing import ZopeTestCase
from Products.UWOshMusicRecruiting.config import *
from Products.UWOshMusicRecruiting.tests.testPlone import testPlone

# Import the tested classes
from Products.UWOshMusicRecruiting.content.Visit import Visit

##code-section module-beforeclass #fill in your manual code here
##/code-section module-beforeclass


class testVisit(testPlone):
    """Test-cases for class(es) ."""

    ##code-section class-header_testVisit #fill in your manual code here
    ##/code-section class-header_testVisit

    def afterSetUp(self):
        pass

    def test_testCreateNewVisit(self):
        pass

    # Manually created methods


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testVisit))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer

if __name__ == '__main__':
    framework()


