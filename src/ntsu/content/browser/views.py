from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#from zope.component import getMultiAdapter
from plone import api
from DateTime import DateTime
import transaction
import random
import csv


class UpdateCounter(BrowserView):
    """ Update Counter """

    def __call__(self):
        context = self.context
        portal = api.portal.get()

        counter = portal['resource']['counter']
        old = int(counter.title)
        new = old + random.randint(30,100)
        counter.title = str(new)
        counter.reindexObject(idxs=['Title'])
        transaction.commit()
        return


class VideoView(BrowserView):
    """ Video View """

    index = ViewPageTemplateFile("template/video_view.pt")

    def __call__(self):
        context = self.context
        catalog = context.portal_catalog
        request = self.request
        response = request.response
        portal = api.portal.get()

        self.docs = context.getChildNodes()
        return self.index()


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


class QuestionView(BrowserView):
    """ Cover View """

    index = ViewPageTemplateFile("template/question_view.pt")

    def __call__(self):
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


class ImportQuestion(BrowserView):
    """ Cover View """

    def __call__(self):
        context = self.context
        catalog = context.portal_catalog
        request = self.request
        response = request.response
        portal = api.portal.get()

        qFolder = portal['resource']['question']

        with open('/home/plone/qLib.csv', 'rb') as file:
            for row in csv.DictReader(file):
#                import pdb; pdb.set_trace()
                ans = [row['ans1'], row['ans2']]
                if row.get('ans3'):
                    ans.append(row['ans3'])
                if row.get('ans4'):
                    ans.append(row['ans4'])
                if row.get('ans5'):
                    ans.append(row['ans5'])

                item = api.content.create(
                    type='Question',
                    container=qFolder,
                    title=row['question'],
                    answer=ans,
                    correctAns=row['correct']
                )

        transaction.commit()


class PlayerView(BrowserView):
    """ Player View """

    index = ViewPageTemplateFile("template/player_view.pt")

    def __call__(self):
        return self.index()

