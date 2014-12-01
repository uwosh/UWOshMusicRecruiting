# -*- coding: utf-8 -*-
#
# File: FacultyMember.py
#
# Copyright (c) 2008 by []
# Generator: ArchGenXML Version 2.0-beta10
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import \
    ReferenceBrowserWidget
from Products.ATBackRef.BackReferenceField import BackReferenceField, BackReferenceWidget
from Products.UWOshMusicRecruiting.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

copied_fields = {}
copied_fields['title'] = BaseSchema['title'].copy()
schema = Schema((

    copied_fields['title'],

    StringField(
        name='email',
        widget=StringField._properties['widget'](
            label='Email',
            label_msgid='UWOshMusicRecruiting_label_email',
            i18n_domain='UWOshMusicRecruiting',
        ),
    ),
    BackReferenceField(
        name='visits',
        widget=BackReferenceWidget(
            label='Visits',
            label_msgid='UWOshMusicRecruiting_label_visits',
            i18n_domain='UWOshMusicRecruiting',
        ),
        allowed_types=('Visit',),
        multiValued=1,
        relationship='facultymember_visit',
    ),
),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

FacultyMember_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class FacultyMember(BaseContent, BrowserDefaultMixin):
    """
    """
    _at_rename_after_creation = True
    security = ClassSecurityInfo()
    implements(interfaces.IFacultyMember)

    meta_type = 'FacultyMember'

    schema = FacultyMember_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(FacultyMember, PROJECTNAME)
# end of class FacultyMember

##code-section module-footer #fill in your manual code here
##/code-section module-footer



