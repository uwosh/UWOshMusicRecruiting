# -*- coding: utf-8 -*-
#
# File: School.py
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
copied_fields['title'].widget.label = "Name"
schema = Schema((

    copied_fields['title'],

    ReferenceField(
        name='visits',
        widget=ReferenceBrowserWidget(
            label='Visits',
            label_msgid='UWOshMusicRecruiting_label_visits',
            i18n_domain='UWOshMusicRecruiting',
        ),
        allowed_types=('Visit',),
        multiValued=1,
        relationship='school_visit',
    ),
),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

School_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class School(BaseContent, BrowserDefaultMixin):
    """
    """
    _at_rename_after_creation = True
    security = ClassSecurityInfo()
    implements(interfaces.ISchool)

    meta_type = 'School'

    schema = School_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(School, PROJECTNAME)
# end of class School

##code-section module-footer #fill in your manual code here
##/code-section module-footer



