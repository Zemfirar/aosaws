from time import sleep
import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import aos_methods as methods
import aos_locators as locators


class AOSTestCases(unittest.TestCase):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("window-size=1400,1500")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("start-maximized")
    options.add_argument("enable-automation")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")

    def setUp(self):
        self.driver = webdriver.Chrome(options=self.options)
        methods.set_up(self.driver)

    def tearDown(self):
        methods.tear_down(self.driver)

    def test_create_new_account(self):
        methods.create_new_account(self.driver, locators.new_username, locators.new_password)
        methods.log_out(self.driver, locators.new_username)
        methods.log_in(self.driver, locators.new_username, locators.new_password)
        methods.log_out(self.driver, locators.new_username)

    def test_validate_homepage_items(self):
        sleep(2)
        methods.validate_homepage_text(self.driver)
        methods.validate_nav_bar_links(self.driver)
        methods.validate_logo_is_displayed(self.driver)
        methods.contact_us(self.driver)

    def test_validate_social_media_links(self):
        sleep(2)
        methods.validate_social_media_links(self.driver)
