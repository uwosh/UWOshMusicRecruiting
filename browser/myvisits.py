"""A report of recently modified cinemas and films
"""

from DateTime import DateTime

from Acquisition import aq_inner

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName


from plone.memoize.instance import memoize

class MyVisitsView(BrowserView):
    """View for showing recent cinema and film modifications
    """
        
    template = ViewPageTemplateFile('my_visits.pt')
        
    def __call__(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)
        
        # Ensure we have a sensible number for days; since this is a non-
        # critical field, we fall silent back on the default if the input is
        # invalid

        return self.template()
        
    def test(self, condition, ifTrue, ifFalse):
        if condition:
            return ifTrue
        else:
            return ifFalse