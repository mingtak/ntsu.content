# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import ntsu.content


class NtsuContentLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=ntsu.content)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ntsu.content:default')


NTSU_CONTENT_FIXTURE = NtsuContentLayer()


NTSU_CONTENT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(NTSU_CONTENT_FIXTURE,),
    name='NtsuContentLayer:IntegrationTesting'
)


NTSU_CONTENT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(NTSU_CONTENT_FIXTURE,),
    name='NtsuContentLayer:FunctionalTesting'
)


NTSU_CONTENT_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        NTSU_CONTENT_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='NtsuContentLayer:AcceptanceTesting'
)
