import pytest
from selenium import webdriver
import utils
import requests
import time
import allure

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from pages.login_page import LoginPage
from pages.main_page import MainPage
from locators import MainPageLocators
from urls import Url


def pytest_addoption(parser):
    parser.addoption("--browser", action="store")


@pytest.fixture()
def driver(request):
    """Создаёт и настраивает веб-драйвер выбранного браузера"""
    browser = request.config.getoption("--browser")

    if browser and 'chrome' in browser.lower():
        driver = webdriver.Chrome()
    elif browser and 'firefox' in browser.lower():
        driver = webdriver.Firefox()
    else:
        raise ValueError('Указан неверный браузер')

    driver.maximize_window()
    driver.set_page_load_timeout(60)
    driver.implicitly_wait(5)
    driver.get(Url.MAIN_PAGE)

    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def user_data():
    max_attempts = 8
    attempt = 0
    access_token = None
    user = None

    while attempt < max_attempts:
        attempt += 1
        user = utils.generate_user_data()

        response = requests.post(
            Url.MAIN_PAGE + Url.CREATE_USER_ENDPOINT,
            json=user,
            proxies=None,
            verify=False,
            timeout=15
        )

        if response.status_code == 200 and response.json().get("success") is True:
            access_token = response.json().get("accessToken")
            break

        elif response.status_code == 403 and "User already exists" in response.text:
            continue

    # Если не удалось создать — возвращаем None (тесты сами решат, что делать)
    if not access_token:
        return None

    yield {
        "user": user,
        "access_token": access_token
    }

    # Очистка: удаление пользователя после теста
    if access_token:
        try:
            requests.delete(
                Url.MAIN_PAGE + Url.DELETE_USER_ENDPOINT,
                headers={'Authorization': access_token},
                proxies=None,
                verify=False,
                timeout=10
            )
        except Exception:
            pass  # ошибки очистки не влияют на тест


@pytest.fixture()
def login_user(driver, user_data):
    if not user_data:
        return False  # пользователь не создан — авторизация невозможна

    main_page = MainPage(driver)
    main_page.enter_in_account()

    login_page = LoginPage(driver)
    login_page.login_user(user_data["user"])

    # Просто ждём кнопку (без raise)
    try:
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located(MainPageLocators.CREATE_ORDER)
        )
        return True
    except:
        allure.attach(
            driver.get_screenshot_as_png(),
            name="После логина нет кнопки 'Оформить заказ'",
            attachment_type=allure.attachment_type.PNG
        )
        return False