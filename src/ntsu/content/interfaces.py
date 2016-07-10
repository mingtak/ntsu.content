# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from ntsu.content import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class INtsuContentLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IPlayer(Interface):

    title = schema.TextLine(
        title=_(u"Title"),
        required=True,
    )

    players = schema.List(
        title=_(u"Players"),
        value_type = schema.TextLine(title=_(u"Players"),),
        required=False,
    )


class IQuestion(Interface):

    title = schema.TextLine(
        title=_(u"Title (Question) "),
        required=True,
    )

    answer = schema.List(
        title=_(u"Answer"),
        value_type = schema.TextLine(title=_(u"Answer"),),
        required=True,
    )

    correctAns = schema.TextLine(
        title=_(u"Correct Answer"),
        required=True,
    )
