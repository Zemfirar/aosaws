import datetime
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

import aos_locators
import aos_locators as locators


def set_up(driver):
    print(f'\nTest started at: {datetime.datetime.now()}')

    driver.maximize_window()

    # to wait for the web browser implicitly
    driver.implicitly_wait(30)

    driver.get(locators.AOS_URL)
    sleep(3)

    # Check that the url address and the title are correct
    if (driver.current_url == locators.AOS_URL or driver.current_url == f'{locators.AOS_URL}#/') \
            and driver.title == locators.AOS_TITLE:
        print(f'We are at the correct web page: {driver.current_url}')
        print(f"We are seeing the correct title page: '{driver.title}'")
    else:
        print(f'We are not at the correct home page. Try again/check your code')
        driver.close()  # close the current tab
        driver.quit()  # close the browser completely


def tear_down(driver):
    if driver is not None:
        print(f'--------------------')
        print(f'Test was completed at: {datetime.datetime.now()}')
        driver.close()
        driver.quit()


def open_user_menu(driver):
    WebDriverWait(driver, 10).until(
        expected_conditions.element_to_be_clickable((By.ID, "menuUserLink"))
    ).click()


def validate_user_logged_in(driver, username):
    assert driver.find_element(
        by=By.XPATH, value="//a[@id='menuUserLink']/span"
    ).text == username


def create_new_account(driver, username, password):
    # WebDriverWait(driver, 10).until(
    #     lambda x: x.find_element(By.ID, "menuUserLink").is_displayed()
    # )
    # driver.find_element(by=By.ID, value='menuUserLink').click()
    open_user_menu(driver)
    sleep(1)

    driver.find_element(by=By.LINK_TEXT, value='CREATE NEW ACCOUNT').click()
    print('Navigating to Create New Account page')
    sleep(1)

    assert driver.find_element(
        by=By.XPATH, value="//h3[.='CREATE ACCOUNT']"
    ).is_displayed()

    driver.find_element(
        by=By.XPATH, value="//input[@name='usernameRegisterPage']"
    ).send_keys(username)
    driver.find_element(
        by=By.XPATH, value="//input[@name='emailRegisterPage']"
    ).send_keys(locators.email)

    driver.find_element(
        by=By.XPATH, value="//input[@name='passwordRegisterPage']"
    ).send_keys(password)
    driver.find_element(
        by=By.XPATH, value="//input[@name='confirm_passwordRegisterPage']"
    ).send_keys(password)

    sleep(1)

    # WebDriverWait(driver, 10).until(
    #     expected_conditions.element_to_be_clickable(
    #         (By.XPATH, "//sec-view[@sec-name='registrationAgreement']")
    #     )
    # ).click()
    # driver.find_element(
    #     by=By.XPATH, value="//sec-view[@sec-name='registrationAgreement']"
    # ).click()
    # driver.find_element(
    #     by=By.XPATH, value="//input[@name='i_agree']"
    # ).click()
    agreement_checkbox = driver.find_element(
        by=By.XPATH, value="//sec-view[@sec-name='registrationAgreement']"
    )
    register_button = driver.find_element(By.ID, "register_btnundefined")
    while "invalid" in register_button.get_attribute("class"):
        # print("register_button is not clickable")
        agreement_checkbox.click()
        sleep(0.5)

    print('Entered information about the new user')

    driver.find_element(By.ID, "register_btnundefined").click()
    print('Creating new user now')
    sleep(2)

    validate_user_logged_in(driver, locators.new_username)

    print(f'New user {username} successfully created')


def log_in(driver, username, password):
    open_user_menu(driver)

    print(f'Going to log in user {username} now')

    driver.find_element(
        by=By.XPATH, value="//input[@name='username']"
    ).send_keys(username)

    driver.find_element(
        by=By.XPATH, value="//input[@name='password']"
    ).send_keys(password)

    driver.find_element(By.ID, "sign_in_btnundefined").click()
    sleep(1)

    print(f'Successfully logged in user {username}')


def log_out(driver, username):
    driver.find_element(
        by=By.XPATH, value="//a[@id='menuUserLink']/span"
    ).click()
    sleep(0.5)

    print('Going to log out now')

    driver.find_element(
        by=By.XPATH,
        value="//div[@id='loginMiniTitle']/label[@translate='Sign_out']"
    ).click()
    sleep(2)

    # look for username element (should be none of them)
    username_menu_elements = driver.find_elements(
            by=By.XPATH, value=f"//a[@id='menuUserLink']/span[.='{username}']"
        )

    assert len(username_menu_elements) == 0

    print('Successfully logged out')


def validate_homepage_text(driver, ):
    print("Validating text on the homepage")

    text_list = ['SPEAKERS', 'TABLETS', 'LAPTOPS', 'MICE', 'HEADPHONES']

    for text in text_list:
        # if element is not found, exception is raised
        driver.find_element(By.ID, f"{text.lower()}Txt")
        print(f"Found {text} on the home page")


def validate_nav_bar_links(driver):
    print("Validating top navigation bar links on the homepage")

    links_text = ['SPECIAL OFFER', 'POPULAR ITEMS', 'CONTACT US', 'OUR PRODUCTS']
    for link_text in links_text:
        driver.find_element(by=By.LINK_TEXT, value=link_text).click()
        print(f"Found {link_text} in the navigation bar")
        sleep(1)


def validate_logo_is_displayed(driver):
    print("Validating logo is displayed on the homepage")

    # logo svg is displayed
    assert driver.find_element(
        by=By.XPATH, value="//div[@class='logo']/a/*[@id='Layer_1']"
    ).is_displayed()

    # dvantage part of logo is displayed
    dvantage_logo = driver.find_element(by=By.XPATH, value="//div[@class='logo']/a/span[1]")
    assert dvantage_logo.text == 'dvantage'

    print("Found logo on the homepage")


def contact_us(driver):
    print("Validating 'Contact Us' form on the homepage")

    Select(driver.find_element(By.XPATH, "//select[@name='categoryListboxContactUs']"))\
        .select_by_visible_text('Laptops')
    Select(driver.find_element(By.XPATH, "//select[@name='productListboxContactUs']")) \
        .select_by_visible_text('HP Chromebook 14 G1(ES)')
    driver.find_element(By.XPATH, "//input[@name='emailContactUs']")\
        .send_keys(aos_locators.email)
    driver.find_element(By.XPATH, "//textarea[@name='subjectTextareaContactUs']") \
        .send_keys(aos_locators.contact_us_subject)

    print("Going to submit 'Contact Us' form")
    driver.find_element(By.ID, 'send_btnundefined').click()
    sleep(0.5)
    assert driver.find_element(By.ID, 'registerSuccessCover').is_displayed()
    assert driver.find_element(
        By.XPATH, "//div[@id='registerSuccessCover']//p"
    ).text == 'Thank you for contacting Advantage support.'

    print("Form successfully submitted")

    continue_shopping_button = driver.find_element(By.XPATH, "//div[@id='registerSuccessCover']//a")
    assert continue_shopping_button.text == 'CONTINUE SHOPPING'
    WebDriverWait(driver, 2).until(
        expected_conditions.element_to_be_clickable(continue_shopping_button)
    ).click()

    print("Continue Shopping button was clicked successfully")


def validate_social_media_links(driver):
    print("Validating social media links on the bottom of the homepage")

    follow_div_xpath = "//div[@id='follow']"
    social_media_links_info = [
        (1, 'facebook.com'), (2, 'twitter.com'), (3, 'linkedin.com')
    ]

    for child_idx, url in social_media_links_info:
        link_to_click = driver.find_element(By.XPATH, f"{follow_div_xpath}/a[{child_idx}]")
        print(f"Visiting link {link_to_click.get_attribute('href')}")
        driver.execute_script("arguments[0].click();", link_to_click)
        sleep(2)
        driver.switch_to.window(driver.window_handles[1])
        assert url in driver.current_url
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    print("Validated all social media links on the homepage")
