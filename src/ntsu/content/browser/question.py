# -*- coding: utf-8 -*-
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#from zope.component import getMultiAdapter
from plone import api
from DateTime import DateTime
import transaction
import csv
import json
import random


class Thanks(BrowserView):
    """ Thanks page """

    index = ViewPageTemplateFile("template/thanks.pt")

    def __call__(self):
        context = self.context
        catalog = context.portal_catalog
        request = self.request
        response = request.response
        portal = api.portal.get()

        player = portal['resource']['player']

        if not request.get('HTTP_REFERER', '').endswith('@@see_result'):
                response.redirect(portal['event'].absolute_url())
                return

        # 要使用 google 驗證，待網址確定後導入

        data = json.dumps(request.form)
        if player.players:
            player.players.append(data)
        else:
            player.players = [data]

        transaction.commit()
        return self.index()


class SeeResult(BrowserView):
    """ See Result page """

    index = ViewPageTemplateFile("template/see_result.pt")

    def __call__(self):
        context = self.context
        catalog = context.portal_catalog
        request = self.request
        response = request.response
        portal = api.portal.get()

        try:
            uState = json.loads(request.cookies.get('uState'))
        except:
            response.redirect(portal['event'].absolute_url())
            return

        self.amount = 0
        for key in uState:
            if uState[key] == 't':
                self.amount += 20
            elif uState[key] == 'n':
                response.redirect(portal['event'].absolute_url())
                return
        return self.index()


class Confirm(BrowserView):
    """ Confirm answer """

    index = ViewPageTemplateFile("template/confirm_view.pt")

    def get_next(self, uState):
        next = ''
        for nq in uState:
            if uState[nq] == 'n':
                next = nq
        return next


    def __call__(self):
        context = self.context
        catalog = context.portal_catalog
        request = self.request
        response = request.response
        portal = api.portal.get()

        if not (request.form.get('id', None) and request.form.get('ans', None)):
            response.redirect(portal['event'].absolute_url())
            return

        id = request.form.get('id')
        ans = request.form.get('ans')

        try:
            uState = json.loads(request.cookies.get('uState'))
        except:
            response.redirect(portal['event'].absolute_url())
            return

        # 檢查重複作答
        if uState[id] != 'n':
            self.result = 'repeated'
            self.next = self.get_next(uState)
            return self.index()



        brain = catalog({'Type':'Question', 'id':id})
        if not brain or len(brain) > 1:
            response.redirect(portal['event'].absolute_url())
            return
        self.item = brain[0]
        if safe_unicode(self.item.getObject().correctAns) == safe_unicode(ans):
            self.result = True
        else:
            self.result = False


        uState[id] = 't' if self.result else 'f'

        cookieData = json.dumps(uState)
        response.setCookie('uState', cookieData)

        self.next = self.get_next(uState)

        return self.index()


class Entry(BrowserView):
    """ Entry, initial user state """

    def __call__(self):
        context = self.context
        catalog = context.portal_catalog
        request = self.request
        response = request.response
        portal = api.portal.get()

        # 選題目
        tfBrain = catalog({'Type':'Question', 'Subject':'TF'})
        chBrain = catalog({'Type':'Question', 'Subject':'CH'})

        tfCount, chCount = 0, 0
        uState = {}
        while True:
            if tfCount < 3:
                item = random.choice(tfBrain)
                if item.id not in uState:
                    uState[item.id] = 'n'
                    tfCount += 1
            if chCount < 2:
                item = random.choice(chBrain)
                if item.id not in uState:
                    uState[item.id] = 'n'
                    chCount += 1
            if tfCount >= 3 and chCount >= 2:
                break

        cookieData = json.dumps(uState)
        response.setCookie('uState', cookieData)

        # to first question
        brain = catalog({'Type':'Question', 'id':uState.keys()[0]})
        if brain:
            item = brain[0]
            response.redirect(item.getURL())
        else:
            response.redirect(portal.absolute_url())

        return


class QuestionView(BrowserView):
    """ Question View """

    index = ViewPageTemplateFile("template/question_view.pt")

    ### 如果user按reload怎麼處理？
    def __call__(self):
        context = self.context
        catalog = context.portal_catalog
        request = self.request
        response = request.response
        portal = api.portal.get()

        cookie = request.cookies.get("uState", None)
        if cookie is None or not request.get('HTTP_REFERER', ''):
            response.redirect(portal['event'].absolute_url())
            return

        uState = json.loads(cookie)
        if not uState.has_key(context.id):
            response.redirect(portal['event'].absolute_url())
            return

        if uState.get(context.id) != 'n':
            for id in uState:
                if uState[id] == 'n':
                    response.redirect('%s/event/question/%s' % (portal.absolute_url, id))
                    return
            response.redirect(portal['event'].absolute_url())
         

#        if not (request.get('HTTP_REFERER', '').endswith('entry') or request.get('HTTP_REFERER', '').endswith('questions')):
#            response.redirect('/sinopac')
#            return

        return self.index()
