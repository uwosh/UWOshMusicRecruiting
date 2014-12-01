# -*- coding: utf-8 -*-
#
# File: Visit.py
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
from Products.CMFCore import permissions as cmfpermissions
##/code-section module-header

schema = Schema((

    TextField(
        name='notes',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label='Notes',
            label_msgid='UWOshMusicRecruiting_label_notes',
            i18n_domain='UWOshMusicRecruiting',
        ),
        default_output_type='text/html',
    ),
    DateTimeField(
        name='dateOfVisit',
        widget=DateTimeField._properties['widget'](
            label='Dateofvisit',
            label_msgid='UWOshMusicRecruiting_label_dateOfVisit',
            i18n_domain='UWOshMusicRecruiting',
        ),
    ),
    ReferenceField(
        name='facultymembers',
        widget=ReferenceBrowserWidget(
            label='Facultymembers',
            label_msgid='UWOshMusicRecruiting_label_facultymembers',
            i18n_domain='UWOshMusicRecruiting',
        ),
        allowed_types=('FacultyMember',),
        multiValued=0,
        relationship='visit_facultymember',
    ),
    ReferenceField(
        name='students',
        widget=ReferenceBrowserWidget(
            label='Students',
            label_msgid='UWOshMusicRecruiting_label_students',
            i18n_domain='UWOshMusicRecruiting',
        ),
        allowed_types=('Student',),
        multiValued=0,
        relationship='visit_student',
    ),
    ReferenceField(
        name='contacts',
        widget=ReferenceBrowserWidget(
            label='Contacts',
            label_msgid='UWOshMusicRecruiting_label_contacts',
            i18n_domain='UWOshMusicRecruiting',
        ),
        allowed_types=('Contact',),
        multiValued=0,
        relationship='visit_contact',
    ),
    BackReferenceField(
        name='schools',
        widget=BackReferenceWidget(
            label='Schools',
            label_msgid='UWOshMusicRecruiting_label_schools',
            i18n_domain='UWOshMusicRecruiting',
        ),
        allowed_types=('School',),
        multiValued=0,
        relationship='visit_school',
    ),
),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Visit_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Visit(BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IVisit)

    meta_type = 'Visit'

    schema = Visit_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(Visit, PROJECTNAME)
# end of class Visit

##code-section module-footer #fill in your manual code here
##/code-section module-footer



