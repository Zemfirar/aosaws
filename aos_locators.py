from faker import Faker


fake = Faker(locale='en_CA')

AOS_URL = 'https://advantageonlineshopping.com/'
AOS_TITLE = ' Advantage Shopping'

new_username = fake.user_name()
new_password = fake.password()

email = fake.email()

contact_us_subject = fake.sentence(nb_words=5)

