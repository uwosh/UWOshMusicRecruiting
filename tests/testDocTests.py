import unittest
import doctest

from zope.testing import doctestunit
from zope.component import testing, eventtesting
from Products.PloneTestCase import PloneTestCase 
from Testing import ZopeTestCase as ztc

def test_suite():
    return unittest.TestSuite([

        # Demonstrate the main content types
        ztc.ZopeDocFileSuite(
            'README.txt', package='Products.UWOshMusicRecruiting.tests',
            test_class=PloneTestCase.FunctionalTestCase,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),

        ztc.ZopeDocFileSuite(
            'CREATE_VISIT.txt', package='Products.UWOshMusicRecruiting.tests',
            test_class=PloneTestCase.FunctionalTestCase,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),
            
        ztc.ZopeDocFileSuite(
            'TEST_VIEWS.txt', package='Products.UWOshMusicRecruiting.tests',
            test_class=PloneTestCase.FunctionalTestCase,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),
        
        ztc.ZopeDocFileSuite(
            'EDIT_VISIT.txt', package='Products.UWOshMusicRecruiting.tests',
            test_class=PloneTestCase.FunctionalTestCase,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),
        ]
        )

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
