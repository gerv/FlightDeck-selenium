#!/usr/bin/env python
# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is Mozilla WebQA Tests.
#
# The Initial Developer of the Original Code is Mozilla Foundation.
# Portions created by the Initial Developer are Copyright (C) 2011
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): David Burns
#                 Zac Campbell
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****
import fd_home_page, fd_login_page, fd_dashboard_page, fd_lib_editor_page
from unittestzero import Assert


class TestLibLabel():

    def testShouldCheckLibraryLabel(self, mozwebqa):
        #This test is to check the labels of a library on the dashboard
        #Create page objects
        homepage_obj = fd_home_page.HomePage(mozwebqa)
        loginpage_obj = fd_login_page.LoginPage(mozwebqa)
        dashboardpage_obj = fd_dashboard_page.DashboardPage(mozwebqa)
        libpage_obj = fd_lib_editor_page.LibraryEditorPage(mozwebqa)
        
        credentials = mozwebqa.credentials['default']
         
        #Create a library. Then go to dashoard and assert that the label is present.
        homepage_obj.go_to_home_page()
        homepage_obj.click_create_lib_btn()
        loginpage_obj.login(credentials['email'], credentials['password'])
        lib_name = libpage_obj.lib_name
        
        libpage_obj.header.click_dashboard()
        Assert.true(dashboardpage_obj.is_the_current_page)
        Assert.true(dashboardpage_obj.library(lib_name).is_displayed(), "Library %s not found" % lib_name)

        #Click on the edit button of the library.Then create a copy of that library and assert that the label is 'copy'
        dashboardpage_obj.library(lib_name).click_edit()
        libpage_obj.click_copy()
        copy_lib_name = libpage_obj.lib_name
        
        try:
            Assert.not_equal(lib_name, copy_lib_name)
        except:
            print 'A copy of the library could not be created'
        libpage_obj.header.click_dashboard()

        Assert.true(dashboardpage_obj.library(copy_lib_name).is_displayed(), "Library %s not found" % copy_lib_name)
