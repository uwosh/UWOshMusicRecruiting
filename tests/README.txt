========================
 UWOshMusicRecruiting Product Tests
========================

Setting up and logging in
-------------------------

We use zope.testbrowser to simulate browser interaction in order to show
the main flow of pages. This is not a true functional test, because we also
inspect and modify the internal state of the ZODB, but it is a useful way of
making sure we test the full end-to-end process of creating and modifying
content.

    >>> from Products.Five.testbrowser import Browser
	>>> from zope.testbrowser import interfaces
	>>> from zope.interface.verify import verifyObject
    >>> browser = Browser()
    >>> portal_url = self.portal.absolute_url()

The following is useful when writing and debugging testbrowser tests. It lets
us see error messages properly.

    >>> browser.handleErrors = False
    >>> self.portal.error_log._ignored_exceptions = ()

We then turn off the various portlets, because they sometimes duplicate links
and text (e.g. the navtree, the recent recent items listing) that we wish to
test for in our own views. Having no portlets makes things easier.

    >>> from zope.component import getUtility, getMultiAdapter
    >>> from plone.portlets.interfaces import IPortletManager
    >>> from plone.portlets.interfaces import IPortletAssignmentMapping

    >>> left_column = getUtility(IPortletManager, name=u"plone.leftcolumn")
    >>> left_assignable = getMultiAdapter((self.portal, left_column), IPortletAssignmentMapping)
    >>> for name in left_assignable.keys():
    ...     del left_assignable[name]

    >>> right_column = getUtility(IPortletManager, name=u"plone.rightcolumn")
    >>> right_assignable = getMultiAdapter((self.portal, right_column), IPortletAssignmentMapping)
    >>> for name in right_assignable.keys():
    ...     del right_assignable[name]

Finally, we need to log in as the portal owner, i.e. an administrator user. We
do this from the login page.

    >>> from Products.PloneTestCase.setup import portal_owner, default_password

    >>> browser.open(portal_url + '/login_form?came_from=' + portal_url)
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()

	>>> verifyObject(interfaces.IBrowser, browser)
	True

	>>> "You are now logged in" in browser.contents
	True

Addable content
---------------
Cinema content is managed inside two root content types: A "Cinema Folder"
contains cinemas and information about them. A "Film Folder" contains films.

    >>> browser.open(portal_url)

Ensure all folders are in folder root

	>>> 'VisitFolder' in self.portal.objectIds()
	True
	>>> 'ContactFolder' in self.portal.objectIds()
	True
	>>> 'StudentFolder' in self.portal.objectIds()
	True
	>>> 'FacultyMemberFolder' in self.portal.objectIds()
	True
	>>> 'SchoolFolder' in self.portal.objectIds()
	True
	
	
Verify all links are present

    >>> schools_link = browser.getLink('Schools')
	>>> verifyObject(interfaces.ILink, schools_link)
	True
	>>> schools_link
	<Link text='Schools' url='http://nohost/plone/SchoolFolder'>
	
	>>> students_link = browser.getLink('Students')
	>>> verifyObject(interfaces.ILink, students_link)
	True
	>>> students_link
	<Link text='Students' url='http://nohost/plone/StudentFolder'>
	
	>>> contacts_link = browser.getLink('Contacts')
	>>> verifyObject(interfaces.ILink, contacts_link)
	True
	>>> contacts_link
	<Link text='Contacts' url='http://nohost/plone/ContactFolder'>
	
	>>> faculty_link = browser.getLink('FacultyMembers')
	>>> verifyObject(interfaces.ILink, faculty_link)
	True
	>>> faculty_link
	<Link text='FacultyMembers' url='http://nohost/plone/FacultyMemberFolder'>
	
	>>> visits_link = browser.getLink(url='VisitFolder', text="Visits")
	>>> verifyObject(interfaces.ILink, visits_link)
	True
	>>> visits_link
	<Link text='Visits' url='http://nohost/plone/VisitFolder'>

	>>> my_visits_link = browser.getLink('My Visits')
	>>> verifyObject(interfaces.ILink, my_visits_link)
	True
	>>> my_visits_link
	<Link text='My Visits' url='http://nohost/plone/my-visits'>
	
	>>> my_instruments_link = browser.getLink('My Instruments')
	>>> verifyObject(interfaces.ILink, my_instruments_link)
	True
	>>> my_instruments_link
	<Link text='My Instruments' url='http://nohost/plone/my-instruments'>
	
	>>> export_visits_link = browser.getLink('Export My Visits')
	>>> verifyObject(interfaces.ILink, export_visits_link)
	True
	>>> export_visits_link
	<Link text='Export My Visits' url='http://nohost/plone/export_user_visits'>
	
	>>> create_new_visit_link = browser.getLink('Create New Visit')
	>>> verifyObject(interfaces.ILink, create_new_visit_link)
	True
	>>> create_new_visit_link.url.endswith("createObject?type_name=Visit")
	True


Create Student

	>>> students_link.click()
	>>> browser.getLink('Add Student').click()
	
	>>> browser.getControl(name="title").value = "New Student"
	>>> browser.getControl(name="form_submit").click()

	>>> students = self.portal['StudentFolder']
	>>> students[students.objectIds()[0]].Title()
	'New Student'

	>>> browser.open(portal_url)
	
Create Contact

	>>> browser.getLink('Contacts').click()
	>>> browser.getLink('Add Contact').click()
	
	>>> browser.getControl(name="title").value = "New Contact"
	>>> browser.getControl(name="form_submit").click()
	
	>>> contacts = self.portal['ContactFolder']
	>>> contacts[contacts.objectIds()[0]].Title()
	'New Contact'

	>>> browser.open(portal_url)
	
Create Faculty

	>>> browser.getLink('FacultyMembers').click()
	>>> browser.getLink('Add FacultyMember').click()
	
	>>> browser.getControl(name="title").value = "New Faculty"
	>>> browser.getControl(name="form_submit").click()

	>>> faculty = self.portal['FacultyMemberFolder']
	>>> faculty[faculty.objectIds()[0]].Title()
	'New Faculty'

	>>> browser.open(portal_url)
	
Create School

	>>> browser.getLink('Schools').click()
	>>> browser.getLink('Add School').click()
	
	>>> browser.getControl(name="title").value = "New School"
	>>> browser.getControl(name="form_submit").click()

	>>> schools = self.portal['SchoolFolder']
	>>> schools[schools.objectIds()[0]].Title()
	'New School'

	>>> browser.open(portal_url)
	
These links should not be present if the user does not have privileges 

	>>> browser.getLink('Log out').click()
	>>> browser.open(portal_url)

	>>> browser.getLink('My Visits')
	Traceback (most recent call last):
	...
	LinkNotFoundError
	
	>>> my_instruments_link = browser.getLink('My Instruments')
	Traceback (most recent call last):
	...
	LinkNotFoundError
	
	>>> export_visits_link = browser.getLink('Export My Visits')
	Traceback (most recent call last):
	...
	LinkNotFoundError
	
	>>> create_new_visit_link = browser.getLink('Create New Visit')
	Traceback (most recent call last):
	...
	LinkNotFoundError

	
	
	
	
	