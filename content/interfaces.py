# -*- coding: utf-8 -*-

from zope.interface import Interface

##code-section HEAD
from zope import schema
from zope.app.container.constraints import contains
##/code-section HEAD

class Istirng(Interface):
    """Marker interface for .stirng.stirng
    """

class Icity(Interface):
    """Marker interface for .city.city
    """

class IVisit(Interface):
    """Marker interface for .Visit.Visit
    """

class IVisitFolder(Interface):
    """Marker interface for .VisitFolder.VisitFolder
    """
    contains('UWOshMusicRecruiting.content.interfaces.IVisit')
    
class IFacultyMember(Interface):
    """Marker interface for .FacultyMember.FacultyMember
    """

class IFacultyMemberFolder(Interface):
    """Marker interface for .FacultyMemberFolder.FacultyMemberFolder
    """

    contains('UWOshMusicRecruiting.content.interfaces.IFacultyMember')

class IStudent(Interface):
    """Marker interface for .Student.Student
    """

class IStudentFolder(Interface):
    """Marker interface for .StudentFolder.StudentFolder
    """

    contains('UWOshMusicRecruiting.content.interfaces.IStudent')

class ISchool(Interface):
    """Marker interface for .School.School
    """

class ISchoolFolder(Interface):
    """Marker interface for .SchoolFolder.SchoolFolder
    """

    contains('UWOshMusicRecruiting.content.interfaces.ISchool')

class IContact(Interface):
    """Marker interface for .Contact.Contact
    """

class IContactFolder(Interface):
    """Marker interface for .ContactFolder.ContactFolder
    """

    contains('UWOshMusicRecruiting.content.interfaces.IContact')

##code-section FOOT
##/code-section FOOT