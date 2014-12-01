# -*- coding: utf-8 -*-
#
# File: testSetup.py
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
# Setup tests
#

import os, sys
from Testing import ZopeTestCase
from Products.UWOshMusicRecruiting.tests.testPlone import testPlone
from Products.CMFCore.utils import getToolByName

class testSetup(testPlone):
    """Test cases for the generic setup of the product."""

    ##code-section class-header_testSetup #fill in your manual code here
    ##/code-section class-header_testSetup

    def afterSetUp(self):
        ids = self.portal.objectIds()

    def test_tools(self):
        ids = self.portal.objectIds()
        self.failUnless('archetype_tool' in ids)

    def test_types(self):
        ids = self.portal.portal_types.objectIds()
        self.failUnless('Visit' in ids)
        self.failUnless('VisitFolder' in ids)
        self.failUnless('Student' in ids)
        self.failUnless('StudentFolder' in ids)
        self.failUnless('Contact' in ids)
        self.failUnless('ContactFolder' in ids)
        self.failUnless('FacultyMember' in ids)
        self.failUnless('FacultyMemberFolder' in ids)
        self.failUnless('School' in ids)
        self.failUnless('SchoolFolder' in ids)
        
    def test_role_added(self):
        self.failUnless('musicFacultyMember' in self.portal.validRoles())

    def test_skins(self):
        ids = self.portal.portal_skins.objectIds()
        
        self.failUnless('uwoshmusicrecruiting_images' in ids)
        self.failUnless('uwoshmusicrecruiting_styles' in ids)
        self.failUnless('uwoshmusicrecruiting_templates' in ids)
        
    def test_templates_in_skins(self): 
        ids = self.portal.portal_skins["uwoshmusicrecruiting_templates"].objectIds()
        
        self.failUnless('create_new_visit_action' in ids)
        self.failUnless('create_new_visit_validate' in ids)
        self.failUnless('import_my_visits' in ids)
        self.failUnless('import_visits_action' in ids)
        self.failUnless('import_visits_validate' in ids)
        self.failUnless('modified_contact_tabular_view' in ids)
        self.failUnless('modified_student_tabular_view' in ids)
        self.failUnless('modified_visit_tabular_view' in ids)
        self.failUnless('modified_edit' in ids)
        self.failUnless('modified_edit_macros' in ids)
        self.failUnless('personalize_form' in ids)

    def test_external_methods_added(self):
        ids = self.portal.portal_skins.custom.objectIds()

        self.failUnless('export_all_visits' in ids) 
        self.failUnless('export_user_visits' in ids)
        self.failUnless('import_visits' in ids)
        self.failUnless('mail_by_instrument_type' in ids)

    def test_permissions_added_to_external_methods(self):
        em = self.portal.portal_skins.custom['export_all_visits']
        self.failUnless('View' in [r['name']] for r in em.permissionsOfRole('musicFacultyMember') if r['selected'])
        self.failUnless('Access contents information' in [r['name']] for r in em.permissionsOfRole('musicFacultyMember') if r['selected'])
        
        em = self.portal.portal_skins.custom['export_user_visits']
        self.failUnless('View' in [r['name']] for r in em.permissionsOfRole('musicFacultyMember') if r['selected'])
        self.failUnless('Access contents information' in [r['name']] for r in em.permissionsOfRole('musicFacultyMember') if r['selected'])
        
        em = self.portal.portal_skins.custom['import_visits']
        self.failUnless('View' in [r['name']] for r in em.permissionsOfRole('musicFacultyMember') if r['selected'])
        self.failUnless('Access contents information' in [r['name']] for r in em.permissionsOfRole('musicFacultyMember') if r['selected'])
        
        em = self.portal.portal_skins.custom['mail_by_instrument_type']
        self.failUnless('View' in [r['name']] for r in em.permissionsOfRole('musicFacultyMember') if r['selected'])
        self.failUnless('Access contents information' in [r['name']] for r in em.permissionsOfRole('musicFacultyMember') if r['selected'])
        
    def test_workflows(self):
        ids = self.portal.portal_workflow.objectIds()
        self.failUnless('UWOshMusicRecruitingWorkFlow' in ids)
        print self.portal.portal_url

    def test_role_added_to_permission(self):
        self.failUnless('Add UWOshMusicRecruiting Content' in [r['name']] for r in self.portal.permissionsOfRole('musicFacultyMember') if r['selected'])
        
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testSetup))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer

if __name__ == '__main__':
    framework()


