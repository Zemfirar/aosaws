from faker import Faker


fake = Faker(locale='en_CA')

AOS_URL = 'https://advantageonlineshopping.com/'
AOS_TITLE = ' Advantage Shopping'

email = fake.email()
contact_us_subject = fake.sentence(nb_words=5)

# existing user info
# username = 'testuser9988'
# password = 'As4RL7D5eW6m'
# email = 'testuser9988@world.com'
# first_name = 'Katarina'
# last_name = 'Witt'
# phone_number = '4568881743'
# country = 'Canada'
# city = 'Vancouver'
# province = 'BC'
# street_address = '1100 Robson St'
# postal_code = 'V6E 1B2'
# payment_method_username = "testuser9988"
# payment_method_password = "TestUser9988"


def get_new_user():
    new_user = [
        fake.user_name(),  # 0
        fake.password(),  # 1
        fake.email(),  # 2
        fake.first_name(),  # 3
        fake.last_name(),  # 4
        fake.phone_number(),  # 5
        'Canada',  # 6
        fake.city(),  # 7
        'BC',  # 8
        fake.street_address(),  # 9
        'V6E 1B2',  # 10
        'safepaypassword',  # 11
        'SafePayPwd1'  # 12
    ]

    return new_user


def get_full_name(first_name, last_name):
    return f"{first_name} {last_name}"
