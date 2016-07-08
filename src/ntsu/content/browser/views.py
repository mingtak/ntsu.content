from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#from zope.component import getMultiAdapter
from plone import api
from DateTime import DateTime
import transaction


class CoverView(BrowserView):
    """ Cover View """

    index = ViewPageTemplateFile("template/cover_view.pt")

    def __call__(self):
        context = self.context
        catalog = context.portal_catalog
        request = self.request
        response = request.response
        portal = api.portal.get()

        self.brain = catalog({'Type':'News Item'}, sort_on='created', sort_order='reverse')
        return self.index()


class OnlineReading(BrowserView):
    """ Online Reading """

    index = ViewPageTemplateFile("template/online_reading.pt")

    def __call__(self):
        context = self.context
        request = self.request
        response = request.response
        portal = api.portal.get()

        return self.index()
