import datetime
import random
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

    print(f'Successfully logged in user {username}')


def create_new_account(driver, user):
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
    ).send_keys(user[0])
    driver.find_element(
        by=By.XPATH, value="//input[@name='emailRegisterPage']"
    ).send_keys(user[2])

    driver.find_element(
        by=By.XPATH, value="//input[@name='passwordRegisterPage']"
    ).send_keys(user[1])
    driver.find_element(
        by=By.XPATH, value="//input[@name='confirm_passwordRegisterPage']"
    ).send_keys(user[1])

    driver.find_element(
        by=By.XPATH, value="//input[@name='first_nameRegisterPage']"
    ).send_keys(user[3])
    driver.find_element(
        by=By.XPATH, value="//input[@name='last_nameRegisterPage']"
    ).send_keys(user[4])
    driver.find_element(
        by=By.XPATH, value="//input[@name='phone_numberRegisterPage']"
    ).send_keys(user[5])
    Select(driver.find_element(By.XPATH, "//select[@name='countryListboxRegisterPage']")) \
        .select_by_visible_text(user[6])
    driver.find_element(
        by=By.XPATH, value="//input[@name='cityRegisterPage']"
    ).send_keys(user[7])
    driver.find_element(
        by=By.XPATH, value="//input[@name='addressRegisterPage']"
    ).send_keys(user[9])
    driver.find_element(
        by=By.XPATH, value="//input[@name='state_/_province_/_regionRegisterPage']"
    ).send_keys(user[8])
    driver.find_element(
        by=By.XPATH, value="//input[@name='postal_codeRegisterPage']"
    ).send_keys(user[10])

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

    validate_user_logged_in(driver, user[0])

    print(f'New user {user[0]} successfully created')


def delete_user_account(driver, user):
    open_user_menu(driver)
    sleep(1)

    driver.find_element(
        by=By.XPATH,
        value="//div[@id='loginMiniTitle']/label[@translate='My_account']"
    ).click()
    sleep(2)

    print("Navigated to the My Account page.")

    found_full_name = driver.find_element(
        by=By.XPATH, value="//div[@id='myAccountContainer']//div[1]/div[1]/div[1]/label"
    ).text

    expected_full_name = locators.get_full_name(user[3], user[4])
    assert found_full_name == expected_full_name
    print(f"Verified full name is displayed: {found_full_name}")

    print("About to delete User Account")
    driver.find_element(
        by=By.XPATH, value="//div[@class='deleteBtnText']/parent::button"
    ).click()

    driver.find_element(
        by=By.XPATH, value="//div[@class='deletePopupBtn deleteRed']"
    ).click()
    sleep(7)

    log_in(driver, user[0], user[1])

    result_message = driver.find_element(By.ID, "signInResultMessage").text
    assert result_message == "Incorrect user name or password."

    print(f"Verified user '{user[0]}' deleted successfully")


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


def log_in_when_checking_out(driver, username, password):
    driver.find_element(By.XPATH, "//input[@name='usernameInOrderPayment']").send_keys(username)
    driver.find_element(By.XPATH, "//input[@name='passwordInOrderPayment']").send_keys(password)
    driver.find_element(By.ID, 'login_btnundefined').click()


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


def validate_item_in_cart(driver, product_description):
    cart_row_xpath = "//div[@id='shoppingCart']/table/tbody/tr[1]"
    cart_product_description = driver.find_element(By.XPATH, f"{cart_row_xpath}/td[2]/label").text.lower()
    assert cart_product_description == product_description
    cart_product_quantity = driver.find_element(By.XPATH, f"{cart_row_xpath}/td[5]/label[2]").text
    assert cart_product_quantity == "1"
    print(f'Found {cart_product_quantity} of {cart_product_description} in the cart')


def validate_item_ordered_page(driver, user):
    thank_you_message = 'Thank you for buying with Advantage'
    assert driver.find_element(
        By.XPATH, "//span[@translate='Thank_you_for_buying_with_Advantage']"
    ).text == thank_you_message, f"Unable to find '{thank_you_message}' message"
    print(f"Verified '{thank_you_message}' message is displayed")

    tracking_number = driver.find_element(By.ID, 'trackingNumberLabel').text
    order_number = driver.find_element(By.ID, 'orderNumberLabel').text
    print(f"Order details: order number = {order_number}, tracking number = {tracking_number}")

    order_info_xpath = "(//div[@class='innerSeccion'])"

    expected_full_name = locators.get_full_name(user[3], user[4])
    assert driver.find_element(
        By.XPATH, f"{order_info_xpath}[1]/label"
    ).text == expected_full_name
    print(f"Verified order full name is {expected_full_name}")

    expected_phone_number = user[5]
    assert driver.find_element(
        By.XPATH, f"{order_info_xpath}[3]/label"
    ).text == expected_phone_number
    print(f"Verified phone number for the order: {expected_phone_number}")

    shipping_address = driver.find_elements(By.XPATH, f"{order_info_xpath}[2]/label")
    assert shipping_address[0].text == user[9]
    assert shipping_address[1].text == user[7]
    assert shipping_address[2].text == user[8]
    print('Validated shipping information')

    order_date = driver.find_element(By.XPATH, f"{order_info_xpath}[5]/label/a").text
    print(f"Order date: {order_date}")
    total_amount = driver.find_element(By.XPATH, f"{order_info_xpath}[6]/label/a").text
    print(f"Order amount: {total_amount}")

    return order_number, total_amount


def validate_my_orders_page(
        driver, expected_product_description, expected_order_number, expected_total_amount
        ):
    order_info_xpath = "//div[@id='myAccountContainer']//table/tbody/tr[2]/td"

    assert driver.find_element(
        By.XPATH, f"{order_info_xpath}[1]/label"
    ).text == expected_order_number

    assert driver.find_element(
        By.XPATH, f"{order_info_xpath}[4]/span"
    ).text.lower() == expected_product_description

    total_amount_in_order_info = driver.find_element(By.XPATH, f"{order_info_xpath}[7]/label").text
    assert total_amount_in_order_info == expected_total_amount, \
        f"Expected total to be {expected_total_amount} but found {total_amount_in_order_info}"

    print(f"Verified order info for order {expected_order_number}")


def add_product_to_cart(driver):
    product_id = random.choice([i for i in range(1, 35) if i != 13])
    product_url = f'{locators.AOS_URL}#/product/{product_id}'

    print(f'Navigating to a product page with product id = {product_id}')
    driver.get(product_url)
    sleep(3)

    product_description = driver.find_element(By.XPATH, "//div[@id='Description']/h1").text.lower()
    print(f'Product description: {product_description}')
    driver.find_element(By.XPATH, "//button[@name='save_to_cart']").click()
    print(f'Added product with id {product_id} to cart')

    return product_description


def remove_product_from_orders(driver, order_number):
    print(f"Going to remove order {order_number}")
    driver.find_element(By.XPATH, "//a[@translate='REMOVE']").click()
    sleep(1)
    driver.find_element(By.XPATH, "//label[contains(text(),'YES')]/parent::button").click()
    sleep(1)
    assert driver.find_element(By.XPATH, "//div[@class='myOrderSection']//label").text == "- No orders -"
    print(f"Verified order {order_number} is removed")


def checkout_shopping_cart(driver, user):
    product_description = add_product_to_cart(driver)
    sleep(1)

    print('Navigating to the shopping cart')
    driver.find_element(By.ID, 'shoppingCartLink').click()
    sleep(1)

    validate_item_in_cart(driver, product_description)

    # start checkout process
    print('Starting checkout process')
    driver.find_element(By.XPATH, "//button[@name='check_out_btn']").click()
    sleep(1)

    # log in while checking out
    log_in_when_checking_out(driver, user[0], user[1])
    sleep(3)

    driver.find_element(By.ID, 'next_btn').click()
    sleep(1)
    print('Navigated to the payment method page')

    driver.find_element(By.XPATH, "//input[@name='safepay_username']").send_keys(user[11])
    driver.find_element(By.XPATH, "//input[@name='safepay_password']").send_keys(user[12])

    pay_now_button = driver.find_element(By.ID, 'pay_now_btn_SAFEPAY')
    assert pay_now_button.is_displayed()
    pay_now_button.click()
    sleep(2)

    order_number, total_amount = validate_item_ordered_page(driver, user)

    log_out(driver, user[0])
    sleep(2)
    log_in(driver, user[0], user[1])
    sleep(4)
    open_user_menu(driver)
    sleep(1)

    print("Navigating to 'My Orders' page")
    driver.find_element(
        by=By.XPATH,
        value="//div[@id='loginMiniTitle']/label[@translate='My_Orders']"
    ).click()
    sleep(2)

    validate_my_orders_page(driver, product_description, order_number, total_amount)

    remove_product_from_orders(driver, order_number)
