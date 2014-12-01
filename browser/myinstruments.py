"""A report of recently modified cinemas and films
"""

from DateTime import DateTime

from Acquisition import aq_inner

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName


from plone.memoize.instance import memoize

class MyInstrumentsView(BrowserView):
    """View for showing recent cinema and film modifications
    """
        
    template = ViewPageTemplateFile('my_instruments.pt')
        
    def __call__(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)
        
        # Ensure we have a sensible number for days; since this is a non-
        # critical field, we fall silent back on the default if the input is
        # invalid

        return self.template()

    def get_all_students_with_instruments(self):

        try:

            portal = getToolByName(self, 'portal_url').getPortalObject()
            pm = getToolByName(portal, 'portal_membership')

            member = pm.getAuthenticatedMember()
            member_instruments = member.getProperty('instrument', None)
            list_of_instruments = member_instruments.split(',')
            list_of_instruments = map(lambda x: x.strip().lower(), list_of_instruments)

            list_of_students = []

            for student in portal.queryCatalog({'portal_type':'Student', 'instrument':list_of_instruments}):
                student = student.getObject()
                if student.getInstrument().strip().lower() in list_of_instruments:
                    list_of_students.append(student)

            return list_of_students
            
        except:
            return None
            
    def test(self, condition, ifTrue, ifFalse):
        if condition:
            return ifTrue
        else:
            return ifFalse