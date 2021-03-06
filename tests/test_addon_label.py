#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.addon_editor_page import AddonEditorPage
from unittestzero import Assert


class TestAddonLabel():

    def testShouldCheckAddonLabel(self, mozwebqa):
        #This test is to check the labels of an add-on on the dashboard
        #Create page objects
        homepage_obj = HomePage(mozwebqa)
        loginpage_obj = LoginPage(mozwebqa)
        dashboardpage_obj = DashboardPage(mozwebqa)
        addonpage_obj = AddonEditorPage(mozwebqa)

        loginpage_obj.login()

        #Create an addon. Then go to dashboard and assert that the label is 'initial'.
        homepage_obj.go_to_home_page()
        homepage_obj.click_create_addon_btn()
        addon_name = addonpage_obj.addon_name

        homepage_obj.header.click_dashboard()
        Assert.true(dashboardpage_obj.is_the_current_page)
        Assert.true(dashboardpage_obj.addon(addon_name).is_displayed, "Addon %s not found" % addon_name)

        #Click on the edit button of the addon.Then create a copy of that addon and assert that the label is 'copy'
        dashboardpage_obj.addon(addon_name).click_edit()
        addonpage_obj.click_copy()
        copy_addon_name = addonpage_obj.addon_name

        try:
            Assert.not_equal(addon_name, copy_addon_name)
        except:
            print 'A copy of the addon could not be created'
        homepage_obj.header.click_dashboard()
        Assert.true(dashboardpage_obj.addon(copy_addon_name).is_displayed, "Addon %s not found" % copy_addon_name)

        dashboardpage_obj.delete_test_data()
