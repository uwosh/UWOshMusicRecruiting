# -*- coding: utf-8 -*-
#
# File: setuphandlers.py
#
# Copyright (c) 2008 by []
# Generator: ArchGenXML Version 2.0-beta10
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'


import logging
logger = logging.getLogger('UWOshMusicRecruiting: setuphandlers')
from Products.UWOshMusicRecruiting.config import PROJECTNAME
from Products.UWOshMusicRecruiting.config import DEPENDENCIES
from Products.CMFCore.utils import getToolByName
from Products.ExternalMethod.ExternalMethod import manage_addExternalMethod

import transaction
##code-section HEAD
def install_external_method(folder, id, description, module, function):
    if not hasattr(folder, id):
        try:
            manage_addExternalMethod(folder, id, description, module, function)
            folder[id].manage_permission("View", roles=["musicFacultyMember", "Manager"], acquire=0)
            folder[id].manage_permission("Access contents information", roles=["musicFacultyMember", "Manager"], acquire=0)
        except:
            logger.info("Error attempting to install %s external method" % (id))
        
def install_tab(existing_tabs, p_actions, all_tab_info):
    for tab_info in all_tab_info:   
        if tab_info[0] in existing_tabs:
            pass
        else:
            p_actions.addAction(tab_info[0], tab_info[1], tab_info[2], tab_info[3], tab_info[4], tab_info[5])
        
def create_folder(context, folder_type, folder_name, id):
    portal = getToolByName(context, 'portal_url').getPortalObject()
    if len(portal.queryCatalog({'portal_type':folder_type, 'title':folder_name, 'id': id})) is 0:
        portal.invokeFactory(id=id, type_name=folder_type)
        portal[id].edit(title=folder_name)

def add_instrument_property(self):
    p_memberdata = getToolByName(self, 'portal_memberdata')
    
    if not p_memberdata.hasProperty('instrument'):
        p_memberdata.manage_addProperty('instrument', '', 'string')
        
def install_external_methods_to_custom_folder(self):
    portal = getToolByName(self, 'portal_url').getPortalObject()
    
    custom_folder = portal.portal_skins.custom
    
    external_methods = \
    [ 
      {'id': 'export_all_visits', 'description': '', 'module': 'UWOshMusicRecruiting.export_visits', 'method': 'export_all_visits' },
      {'id': 'export_user_visits', 'description': '', 'module': 'UWOshMusicRecruiting.export_visits', 'method': 'export_user_visits' },
      {'id': 'import_visits', 'description': '', 'module': 'UWOshMusicRecruiting.import_visits', 'method': 'import_visits' },
      {'id': 'mail_by_instrument_type', 'description': '', 'module': 'UWOshMusicRecruiting.mail_by_instrument_type', 'method': 'mail_by_instrument_type' },
    ]

    for external_method in external_methods:
        install_external_method(custom_folder, external_method['id'], external_method['description'], external_method['module'], external_method['method'])
            
def add_portal_tabs(self):
    p_actions = getToolByName(self, 'portal_actions')
    
    portal = getToolByName(self, 'portal_url').getPortalObject()
    
    visit_folder = portal.queryCatalog({'portal_type':'VisitFolder'})[0].id
    
    # id, title, url, condition, permission, category
    added_buttons = [['create_new_visit_button', 'Create New Visit', 'string:${globals_view/navigationRootUrl}/' +visit_folder+ '/createObject?type_name=Visit', '', 'Add UWOshMusicRecruiting Content', 'portal_tabs'],
                     ['my_visits_button', 'My Visits', 'string:${globals_view/navigationRootUrl}/my-visits','', 'Add UWOshMusicRecruiting Content', 'portal_tabs'], 
                     ['my_instruments_button', 'My Instruments', 'string:${globals_view/navigationRootUrl}/my-instruments', '', 'Add UWOshMusicRecruiting Content', 'portal_tabs'],
                     ['export_my_visits_button', 'Export My Visits', 'string:${globals_view/navigationRootUrl}/export_user_visits','', 'Add UWOshMusicRecruiting Content', 'portal_tabs']]
    
    install_tab(map(lambda x: x.getId(), p_actions.listActions()), p_actions, added_buttons)

def setup_site_properties(self):
    self.portal_properties.site_properties.manage_changeProperties( {'allowRolesToAddKeywords':['Manager', 'Reviewer', 'musicFacultyMember']} )
    self.manage_permission("Add UWOshMusicRecruiting Content", roles=["musicFacultyMember", "Manager"], acquire=0)
    
##/code-section HEAD

def installGSDependencies(context):
    """Install dependend profiles."""

    # XXX Hacky, but works for now. has to be refactored as soon as generic
    # setup allows a more flexible way to handle dependencies.

    shortContext = context._profile_path.split('/')[-3]
    if shortContext != 'UWOshMusicRecruiting':
        # the current import step is triggered too many times, this creates infinite recursions
        # therefore, we'll only run it if it is triggered from proper context
        logger.debug("installGSDependencies will not run in context %s" % shortContext)
        return
    logger.info("installGSDependencies started")
    dependencies = []
    if not dependencies:
        return

    site = context.getSite()
    setup_tool = getToolByName(site, 'portal_setup')
    qi = getToolByName(site, 'portal_quickinstaller')
    for dependency in dependencies:
        logger.info("  installing GS dependency %s:" % dependency)
        if dependency.find(':') == -1:
            dependency += ':default'
        old_context = setup_tool.getImportContextID()
        setup_tool.setImportContext('profile-%s' % dependency)
        importsteps = setup_tool.getImportStepRegistry().sortSteps()
        excludes = [
            u'UWOshMusicRecruiting-QI-dependencies',
            u'UWOshMusicRecruiting-GS-dependencies'
        ]
        importsteps = [s for s in importsteps if s not in excludes]
        for step in importsteps:
            logger.debug("     running import step %s" % step)
            setup_tool.runImportStep(step) # purging flag here?
            logger.debug("     finished import step %s" % step)
        # let's make quickinstaller aware that this product is installed now
        product_name = dependency.split(':')[0]
        qi.notifyInstalled(product_name)
        logger.debug("   notified QI that %s is installed now" % product_name)
        # maybe a savepoint is welcome here (I saw some in optilude's examples)? maybe not? well...
        transaction.savepoint()
        if old_context: # sometimes, for some unknown reason, the old_context is None, believe me
            setup_tool.setImportContext(old_context)
        logger.debug("   installed GS dependency %s:" % dependency)

    # re-run some steps to be sure the current profile applies as expected
    importsteps = setup_tool.getImportStepRegistry().sortSteps()
    filter = [
        u'typeinfo',
        u'workflow',
        u'membranetool',
        u'factorytool',
        u'content_type_registry',
        u'membrane-sitemanager'
    ]
    importsteps = [s for s in importsteps if s in filter]
    for step in importsteps:
        setup_tool.runImportStep(step) # purging flag here?
    logger.info("installGSDependencies finished")

def installQIDependencies(context):
    """This is for old-style products using QuickInstaller"""
    shortContext = context._profile_path.split('/')[-3]
    if shortContext != 'UWOshMusicRecruiting': # avoid infinite recursions
        logger.debug("installQIDependencies will not run in context %s" % shortContext)
        return
    logger.info("installQIDependencies starting")
    site = context.getSite()
    qi = getToolByName(site, 'portal_quickinstaller')

    for dependency in DEPENDENCIES:
        if qi.isProductInstalled(dependency):
            logger.info("   re-Installing QI dependency %s:" % dependency)
            qi.reinstallProducts([dependency])
            transaction.savepoint() # is a savepoint really needed here?
            logger.debug("   re-Installed QI dependency %s:" % dependency)
        else:
            if qi.isProductInstallable(dependency):
                logger.info("   installing QI dependency %s:" % dependency)
                qi.installProduct(dependency)
                transaction.savepoint() # is a savepoint really needed here?
                logger.debug("   installed dependency %s:" % dependency)
            else:
                logger.info("   QI dependency %s not installable" % dependency)
                raise "   QI dependency %s not installable" % dependency
    logger.info("installQIDependencies finished")



def updateRoleMappings(context):
    """after workflow changed update the roles mapping. this is like pressing
    the button 'Update Security Setting' and portal_workflow"""

    shortContext = context._profile_path.split('/')[-3]
    if shortContext != 'UWOshMusicRecruiting': # avoid infinite recursions
        return
    wft = getToolByName(context.getSite(), 'portal_workflow')
    wft.updateRoleMappings()

def postInstall(context):
    """Called as at the end of the setup process. """
    # the right place for your custom code


    shortContext = context._profile_path.split('/')[-3]
    if shortContext != 'UWOshMusicRecruiting': # avoid infinite recursions
        return
    site = context.getSite()

    create_folder(site, 'StudentFolder', 'Students', 'StudentFolder')
    create_folder(site, 'SchoolFolder', 'Schools', 'SchoolFolder')
    create_folder(site, 'ContactFolder', 'Contacts', 'ContactFolder')
    create_folder(site, 'FacultyMemberFolder', 'FacultyMembers', 'FacultyMemberFolder')
    create_folder(site, 'VisitFolder', 'Visits', 'VisitFolder')

    add_instrument_property(site)

    install_external_methods_to_custom_folder(site)

    add_portal_tabs(site)

    setup_site_properties(site)

##code-section FOOT
##/code-section FOOT
