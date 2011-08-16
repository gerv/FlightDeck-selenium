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
from fd_base_page import FlightDeckBasePage
from page import Page
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class DashboardPage(FlightDeckBasePage):

    _home_page_click = 'flightdeck-logo'
    _top_public_addon_name = "//section[@id='app-content']/ul[1]/li[1]/h3"
    _top_public_lib_name = "//section[@id='app-content']/ul[2]/li[1]/h3"

    _public_addons_link = (By.LINK_TEXT, "Public Add-ons")
    _public_libs_link = (By.LINK_TEXT, "Public Libraries")
    _private_addons_link = (By.LINK_TEXT, "Private Add-ons")
    _private_libs_link = (By.LINK_TEXT, "Private Libraries")
   
    _addon = "//ul[preceding-sibling::h2[text()='Your Latest Add-ons']][1]"
    _lib = "//ul[preceding-sibling::h2[text()='Your Latest Libraries']][1]"
    
    _name = "/li[1]/h3"
    _test_btn = "/li[1]/ul/li[@class='UI_Try_in_Browser XPI_test']/a"
    _edit_btn = "/li[1]/ul/li[@class='UI_Edit_Version ']/a"
    _delete_btn = "/li[1]/ul/li[@class='UI_Delete']/a"
    _public_btn = "/li[1]/ul/li/a[@title='Let the world use it']"
    _private_btn = "/li[1]/ul/li/a[@title='My preciousss!']"
      
    _confirm_delete_btn = 'delete_package'
    
    _addons_list = "//section[@id='app-content']/ul[1]/li"
    _libs_list = "//section[@id='app-content']/ul[2]/li"
    _addons_counter = "//aside[@id='app-sidebar']/ul/li[1]/strong"
    _libs_counter = "//aside[@id='app-sidebar']/ul/li[2]/strong"

    def get_top_addon_name(self):
        return self.selenium.find_element_by_xpath(self._addon + self._name).text
    
    def get_top_lib_name(self):
        return self.selenium.find_element_by_xpath(self._lib + self._name).text   

    def get_addons_count(self):
        return self.selenium.find_element_by_xpath(self._addons_counter).text
        
    def calc_total_addons(self):
        elements = self.selenium.find_elements_by_xpath(self._addons_list)
        return len(elements)
        
    def go_to_private_addons_page(self):
        self.selenium.find_element(*self._private_addons_link).click()
    
    def go_to_private_libs_page(self):
        self.selenium.find_element(*self._private_libs_link).click()
    
    def go_to_public_libs_page(self):
        self.selenium.find_element(*self._public_libs_link).click()
    
    def navigate_to_addon_editor(self):
        self.selenium.find_element_by_xpath(self._addon + self._edit_btn).click()
    
    def navigate_to_lib_editor(self):
        self.selenium.find_element_by_xpath(self._lib + self._edit_btn).click()
        
    def check_addon_test_btn_present(self):
        try:
            self.selenium.find_element_by_xpath(self._addon + self._test_btn)
            return True
        except NoSuchElementException:
            return False

    def check_addon_edit_btn_present(self):
        try:
            self.selenium.find_element_by_xpath(self._addon + self._edit_btn)
            return True
        except NoSuchElementException:
            return False
    
    def check_addon_delete_btn_present(self):
        try:
            self.selenium.find_element_by_xpath(self._addon + self._delete_btn)
            return True
        except NoSuchElementException:
            return False
    
    def check_addon_public_btn_present(self):
        try:
            self.selenium.find_element_by_xpath(self._addon + self._public_btn)
            return True
        except NoSuchElementException:
            return False
    
    def check_addon_private_btn_present(self):
        try:
            self.selenium.find_element_by_xpath(self._addon + self._private_btn)
            return True
        except NoSuchElementException:
            return False
    
    def click_addon_mkprivate_btn(self):
        self.selenium.find_element_by_xpath(self._addon + self._private_btn).click()
    
    def click_addon_mkpublic_btn(self):
        self.selenium.find_element_by_xpath(self._addon + self._public_btn).click()
    
    def click_lib_mkprivate_btn(self):
        self.selenium.find_element_by_xpath(self._lib + self._private_btn).click()
        
    def click_lib_mkpublic_btn(self):
        self.selenium.find_element_by_xpath(self._lib + self._public_btn).click()

    def click_addon_delete(self):
        self.selenium.find_element_by_xpath(self._addon + self._delete_btn).click()

    def click_lib_delete(self):
        self.selenium.find_element_by_xpath(self._lib + self._delete_btn).click()
        
    def confirm_delete(self):
        self.selenium.find_element_by_id(self._confirm_delete_btn).click()