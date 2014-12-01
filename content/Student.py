# -*- coding: utf-8 -*-
#
# File: Student.py
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
copied_fields['title'].required = 1
copied_fields['title'].searchable = 1
copied_fields['title'].widget.label = "Name"
schema = Schema((

    copied_fields['title'],

    StringField(
        name='phone',
        widget=StringField._properties['widget'](
            label='Phone',
            label_msgid='UWOshMusicRecruiting_label_phone',
            i18n_domain='UWOshMusicRecruiting',
        ),
        searchable=1,
    ),
    StringField(
        name='email',
        widget=StringField._properties['widget'](
            label='Email',
            label_msgid='UWOshMusicRecruiting_label_email',
            i18n_domain='UWOshMusicRecruiting',
        ),
        searchable=1,
    ),
    StringField(
        name='instrument',
        widget=StringField._properties['widget'](
            label='Instrument',
            label_msgid='UWOshMusicRecruiting_label_instrument',
            i18n_domain='UWOshMusicRecruiting',
        ),
        searchable=1,
    ),
    StringField(
        name='address',
        widget=StringField._properties['widget'](
            label='Address',
            label_msgid='UWOshMusicRecruiting_label_address',
            i18n_domain='UWOshMusicRecruiting',
        ),
        searchable=1,
    ),
    StringField(
        name='city',
        widget=StringField._properties['widget'](
            label='City',
            label_msgid='UWOshMusicRecruiting_label_city',
            i18n_domain='UWOshMusicRecruiting',
        ),
        searchable=1,
    ),
    StringField(
        name='state',
        widget=StringField._properties['widget'](
            label='State',
            label_msgid='UWOshMusicRecruiting_label_state',
            i18n_domain='UWOshMusicRecruiting',
        ),
        searchable=1,
    ),
    StringField(
        name='zip',
        widget=StringField._properties['widget'](
            label='Zip',
            label_msgid='UWOshMusicRecruiting_label_zip',
            i18n_domain='UWOshMusicRecruiting',
        ),
        searchable=1,
    ),
    BooleanField(
        name='isCommittedToAttend',
        widget=BooleanField._properties['widget'](
            label='Iscommittedtoattend',
            label_msgid='UWOshMusicRecruiting_label_isCommittedToAttend',
            i18n_domain='UWOshMusicRecruiting',
        ),
        searchable=1,
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
        relationship='student_visit',
    ),
),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Student_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Student(BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IStudent)

    meta_type = 'Student'
    _at_rename_after_creation = True

    schema = Student_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(Student, PROJECTNAME)
# end of class Student

##code-section module-footer #fill in your manual code here
##/code-section module-footer



