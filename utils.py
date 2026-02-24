import allure
from faker import Faker

@allure.step('Генерация тестовых данных пользователя')
def generate_user_data():
    user_data = {
        "email": Faker().email(),
        "password": Faker().password(),
        "name": Faker().first_name()
    }
    return user_data
