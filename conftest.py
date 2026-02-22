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
    """Создаёт уникального пользователя через API, повторяет попытки при коллизии email"""
    max_attempts = 8
    attempt = 0
    access_token = None

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
            time.sleep(0.3)  # пауза перед следующей попыткой
            continue

        else:
            # Неожиданный ответ — продолжаем пытаться
            continue

    else:
        raise AssertionError(f"Не удалось создать пользователя после {max_attempts} попыток")

    assert access_token, "Не получен accessToken после успешной регистрации"

    yield user

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
    """Выполняет авторизацию и проверяет успешный переход на главную"""
    main_page = MainPage(driver)
    main_page.enter_in_account()

    login_page = LoginPage(driver)
    login_page.login_user(user_data)

    # Убрали time.sleep(2.5)
    # Ждём реальную кнопку оформления заказа или индикатор успешного логина
    try:
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located(MainPageLocators.CREATE_ORDER)
        )
    except:
        allure.attach(
            driver.get_screenshot_as_png(),
            name="После логина нет кнопки 'Оформить заказ'",
            attachment_type=allure.attachment_type.PNG
        )
        raise AssertionError("Кнопка 'Оформить заказ' не появилась после авторизации")

    current_url = driver.current_url
    if "login" in current_url.lower():
        raise AssertionError(f"Остались на странице логина: {current_url}")