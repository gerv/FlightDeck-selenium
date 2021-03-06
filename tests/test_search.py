#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.search_page import SearchPage
from pages.dashboard_page import DashboardPage
from pages.addon_editor_page import AddonEditorPage
from pages.library_editor_page import LibraryEditorPage
from pages.user_page import UserPage
from unittestzero import Assert
import pytest
xfail = pytest.mark.xfail
prod = pytest.mark.prod


class TestSearch():

    def test_search_by_addon_name_returns_addon(self, mozwebqa):
        homepage_obj = HomePage(mozwebqa)
        loginpage_obj = LoginPage(mozwebqa)
        dashboard_obj = DashboardPage(mozwebqa)
        addonpage_obj = AddonEditorPage(mozwebqa)
        searchpage_obj = SearchPage(mozwebqa)

        homepage_obj.go_to_home_page()
        homepage_obj.header.click_signin()
        loginpage_obj.login()

        #create a new addon with the valid criteria (version not initial)
        dashboard_obj.header.click_home_logo()
        homepage_obj.click_create_addon_btn()
        addonpage_obj.type_addon_version('searchable')
        addonpage_obj.click_save()
        searchterm = addonpage_obj.addon_name

        addonpage_obj.header.click_home_logo()
        homepage_obj.header.click_search()

        searchpage_obj.search_until_package_exists(searchterm, searchpage_obj.addon(searchterm))
        Assert.true(searchpage_obj.addon(searchterm).is_displayed, '%s not found before timeout' % searchterm)

        searchpage_obj.delete_test_data()

    def test_search_by_library_name_returns_library(self, mozwebqa):
        homepage_obj = HomePage(mozwebqa)
        loginpage_obj = LoginPage(mozwebqa)
        dashboard_obj = DashboardPage(mozwebqa)
        librarypage_obj = LibraryEditorPage(mozwebqa)
        searchpage_obj = SearchPage(mozwebqa)

        homepage_obj.go_to_home_page()
        homepage_obj.header.click_signin()
        loginpage_obj.login()

        #create a new library with the valid criteria (version not initial)
        dashboard_obj.header.click_home_logo()
        homepage_obj.click_create_lib_btn()
        librarypage_obj.type_library_version('searchable')
        librarypage_obj.click_save()
        searchterm = librarypage_obj.library_name

        librarypage_obj.header.click_home_logo()
        homepage_obj.header.click_search()

        searchpage_obj.search_until_package_exists(searchterm, searchpage_obj.library(searchterm))
        Assert.true(searchpage_obj.library(searchterm).is_displayed, '%s not found before timeout' % searchterm)

        searchpage_obj.delete_test_data()

    @prod
    def test_search_partial_addon_name_returns_addon(self, mozwebqa):
        homepage_obj = HomePage(mozwebqa)
        searchpage_obj = SearchPage(mozwebqa)

        homepage_obj.go_to_home_page()
        homepage_obj.header.click_search()

        # get addon name, split string in half and search with it
        # results should be returned including the original addon

        top_addon_name = searchpage_obj.addon(1).name
        search_string = top_addon_name[:4]
        searchpage_obj.type_search_term(search_string)
        searchpage_obj.click_search()

        Assert.true(searchpage_obj.addons_element_count() >= 1)
        Assert.true(searchpage_obj.addon(top_addon_name).is_displayed, 'Addon \'%s\' not found' % top_addon_name)

    @prod
    def test_search_partial_library_name_returns_library(self, mozwebqa):
        homepage_obj = HomePage(mozwebqa)
        searchpage_obj = SearchPage(mozwebqa)

        homepage_obj.go_to_home_page()
        homepage_obj.header.click_search()

        # get library name, split string in half and search with it
        # results should be returned including the original addon

        top_library_name = searchpage_obj.library(1).name
        search_string = top_library_name[:4]
        searchpage_obj.type_search_term(search_string)
        searchpage_obj.click_search()

        Assert.true(searchpage_obj.library_element_count() >= 1)
        Assert.true(searchpage_obj.library(top_library_name).is_displayed, 'Library \'%s\' not found' % top_library_name)

    @prod
    def test_empty_search_returns_all_results(self, mozwebqa):
        homepage_obj = HomePage(mozwebqa)
        searchpage_obj = SearchPage(mozwebqa)

        homepage_obj.go_to_home_page()
        homepage_obj.header.click_search()

        # search with a zero length string should still return results
        # default display is for 5 addons/5 libraries
        # same as filtering by 'Combined'

        searchpage_obj.clear_search()
        searchpage_obj.click_search()

        Assert.equal(searchpage_obj.addons_element_count(), 5)
        Assert.equal(searchpage_obj.library_element_count(), 5)

    @prod
    def test_search_addon_filter_results_match(self, mozwebqa):
        homepage_obj = HomePage(mozwebqa)
        searchpage_obj = SearchPage(mozwebqa)

        homepage_obj.go_to_home_page()
        homepage_obj.header.click_search()

        # search with a generic but safe string 'test'
        # filter by add-on results and check number

        searchpage_obj.type_search_term('test')
        searchpage_obj.click_search()

        searchpage_obj.click_filter_addons_link()

        # 20 items maximum per page
        label_count = min(searchpage_obj.addons_count_label, 20)
        element_count = searchpage_obj.addons_element_count()

        Assert.equal(label_count, element_count, 'Number of items displayed should match 20 or total number of results, whichever is smallest. This is due to pagination.')

    @prod
    def test_search_library_filter_results_match(self, mozwebqa):
        homepage_obj = HomePage(mozwebqa)
        searchpage_obj = SearchPage(mozwebqa)

        homepage_obj.go_to_home_page()
        homepage_obj.header.click_search()

        # search with a generic but safe string 'test'
        # filter by add-on results and check number

        searchpage_obj.type_search_term('test')
        searchpage_obj.click_search()

        searchpage_obj.click_filter_libraries_link()

        # 20 items maximum per page
        label_count = min(searchpage_obj.library_count_label, 20)
        element_count = searchpage_obj.library_element_count()

        Assert.equal(label_count, element_count, 'Number of items displayed should match 20 or total number of results, whichever is smallest. This is due to pagination.')

    @prod
    def test_clicking_addon_author_link_displays_author_profile(self, mozwebqa):
        # go to addon result and click author link

        homepage_obj = HomePage(mozwebqa)
        userpage_obj = UserPage(mozwebqa)
        searchpage_obj = SearchPage(mozwebqa)

        homepage_obj.go_to_home_page()
        homepage_obj.header.click_search()

        addon_name = searchpage_obj.addon(1).name
        author_name = searchpage_obj.addon(addon_name).author_name
        searchpage_obj.addon(addon_name).click_author()
        Assert.equal(userpage_obj.author_name.lower(), author_name)

    @xfail(reason="Bug 661619 - [traceback] MultipleObjectsReturned: get() returned more than one Profile -- it returned 2! Lookup parameters were {}")
    @prod
    def test_clicking_library_author_link_displays_author_profile(self, mozwebqa):

        # go to library result and click author link
        homepage_obj = HomePage(mozwebqa)
        userpage_obj = UserPage(mozwebqa)
        searchpage_obj = SearchPage(mozwebqa)

        homepage_obj.go_to_home_page()
        homepage_obj.header.click_search()

        library_name = searchpage_obj.library(1).name
        author_name = searchpage_obj.library(library_name).author_name
        searchpage_obj.library(library_name).click_author()
        Assert.equal(userpage_obj.author_name.lower(), author_name)

    def test_clicking_addon_source_displays_editor(self, mozwebqa):
        homepage_obj = HomePage(mozwebqa)
        loginpage_obj = LoginPage(mozwebqa)
        dashboard_obj = DashboardPage(mozwebqa)
        searchpage_obj = SearchPage(mozwebqa)
        editorpage_obj = AddonEditorPage(mozwebqa)

        homepage_obj.go_to_home_page()
        homepage_obj.header.click_signin()
        loginpage_obj.login()
        dashboard_obj.header.click_search()

        addon_name = searchpage_obj.addon(1).name
        searchpage_obj.addon(addon_name).click()
        Assert.equal(editorpage_obj.addon_name, addon_name)

        searchpage_obj.delete_test_data()

    def test_clicking_library_source_displays_editor(self, mozwebqa):
        homepage_obj = HomePage(mozwebqa)
        loginpage_obj = LoginPage(mozwebqa)
        dashboard_obj = DashboardPage(mozwebqa)
        searchpage_obj = SearchPage(mozwebqa)
        editorpage_obj = LibraryEditorPage(mozwebqa)

        homepage_obj.go_to_home_page()
        homepage_obj.header.click_signin()
        loginpage_obj.login()
        dashboard_obj.header.click_search()

        library_name = searchpage_obj.library(1).name
        searchpage_obj.library(library_name).click()
        Assert.equal(editorpage_obj.library_name, library_name)

        searchpage_obj.delete_test_data()

    @prod
    def test_copies_slider_filters_results(self, mozwebqa):
        homepage_obj = HomePage(mozwebqa)
        searchpage_obj = SearchPage(mozwebqa)

        homepage_obj.go_to_home_page()
        homepage_obj.header.click_search()

        initial_addon_count = searchpage_obj.addons_count_label
        initial_library_count = searchpage_obj.library_count_label
        searchpage_obj.move_copies_slider(1)

        Assert.true(initial_addon_count > searchpage_obj.addons_count_label)
        Assert.true(initial_library_count > searchpage_obj.library_count_label)

    @prod
    def test_used_packages_slider_filters_results(self, mozwebqa):
        homepage_obj = HomePage(mozwebqa)
        searchpage_obj = SearchPage(mozwebqa)

        homepage_obj.go_to_home_page()
        homepage_obj.header.click_search()
        searchpage_obj.click_filter_libraries_link()

        initial_library_count = searchpage_obj.library_count_label
        searchpage_obj.move_used_packages_slider(10)

        Assert.true(initial_library_count > searchpage_obj.library_count_label)

    @prod
    def test_activity_slider_filters_results(self, mozwebqa):
        homepage_obj = HomePage(mozwebqa)
        searchpage_obj = SearchPage(mozwebqa)

        homepage_obj.go_to_home_page()
        homepage_obj.header.click_search()

        initial_addon_count = searchpage_obj.addons_count_label
        initial_library_count = searchpage_obj.library_count_label
        searchpage_obj.move_activity_slider(1)

        Assert.true(initial_addon_count > searchpage_obj.addons_count_label)
        Assert.true(initial_library_count > searchpage_obj.library_count_label)
