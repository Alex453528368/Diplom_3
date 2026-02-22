import allure
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from locators import MainPageLocators
from pages.base_page import BasePage
from urls import Url


class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Получить количество добавлений ингредиента")
    def get_ingredient_count(self):
        return self.get_value_from_element(MainPageLocators.INGREDIENT_COUNTER)

    @allure.step("Кликнуть на ингредиент")
    def view_ingredient(self):
        self.click_on_element(MainPageLocators.INGREDIENT)

    @allure.step("Закрыть окно с деталями об ингредиенте")
    def close_ingredient_detail_windows(self):
        self.click_on_element(MainPageLocators.CLOSE_MODAL_WINDOW)

    @allure.step("Проверить открытие окна с деталями ингредиента")
    def check_visible_ingredient_detail_windows(self):
        return self.check_is_visible_element(MainPageLocators.MODAL_WINDOW)

    @allure.step('Перейти на страницу Лента заказов')
    def go_to_orders_feed_page(self):
        self.click_on_element(MainPageLocators.GO_TO_ORDERS_FEED_BTN)
        self.wait_load_url(Url.ORDERS_FEED_PAGE)

    @allure.step('Перейти на страницу Личный кабинет')
    def go_to_profile(self):
        self.click_on_element(MainPageLocators.GO_TO_PROFILE_BTN)
        self.wait_load_url(Url.PROFILE_PAGE)

    @allure.step('Перейти на страницу Авторизация')
    def go_to_login(self):
        self.click_on_element(MainPageLocators.GO_TO_PROFILE_BTN)
        self.wait_load_url(Url.LOGIN_PAGE)

    @allure.step('Добавить ингредиент в корзину')
    def add_ingredient_in_basket(self):
        self.drag_and_drop(
            MainPageLocators.INGREDIENT,
            MainPageLocators.BASKET_AREA
        )
        time.sleep(0.7)  # небольшая пауза помогает Firefox и React-приложениям

    @allure.step('Нажать кнопку Войти в аккаунт')
    def enter_in_account(self):
        self.click_on_element(MainPageLocators.ENTER_IN_ACCOUNT)

    @allure.step('Создать заказ')
    def create_order(self):
        ingredients = self.get_elements(MainPageLocators.INGREDIENT)

        # Добавляем булку
        for ingredient in ingredients:
            text = ingredient.text.lower()
            if 'булка' in text or 'bun' in text:
                self.drag_and_drop(MainPageLocators.INGREDIENT, MainPageLocators.BASKET_AREA)
                time.sleep(0.8)
                break

        # Добавляем любую начинку
        for ingredient in ingredients:
            text = ingredient.text.lower()
            if 'булка' not in text and 'bun' not in text:
                self.drag_and_drop(MainPageLocators.INGREDIENT, MainPageLocators.BASKET_AREA)
                time.sleep(0.8)
                break

        time.sleep(2.0)  # даём время на обновление корзины (важно для Firefox)

        # Проверяем, что кнопка активна
        create_btn = self.get_element(MainPageLocators.CREATE_ORDER)
        if create_btn.get_attribute('disabled') == 'true':
            raise AssertionError("Кнопка 'Оформить заказ' отключена")

        self.click_on_element(MainPageLocators.CREATE_ORDER)

        # Ожидаем появления номера заказа
        self.wait_element(MainPageLocators.ORDER_NUMBER)

        def is_real_order_number():
            try:
                text = self.get_element(MainPageLocators.ORDER_NUMBER).text.strip()
                return text.isdigit() and text != '9999' and len(text) >= 4
            except:
                return False

        try:
            WebDriverWait(self.driver, 35).until(lambda d: is_real_order_number())
        except TimeoutException:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="Модальное окно без номера заказа",
                attachment_type=allure.attachment_type.PNG
            )
            raise AssertionError("Реальный номер заказа не появился")

        order_text = self.get_value_from_element(MainPageLocators.ORDER_NUMBER)
        order_number = order_text.replace('#', '').lstrip('0').strip() or "unknown"

        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Модальное окно с номером заказа",
            attachment_type=allure.attachment_type.PNG
        )

        # Закрытие модального окна + оверлея (надёжная версия для Firefox)
        # 1. Пробуем обычный клик по кнопке закрытия
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(MainPageLocators.CLOSE_MODAL_WINDOW)
            )
            self.click_on_element(MainPageLocators.CLOSE_MODAL_WINDOW)
        except:
            # 2. JS-клик по кнопке закрытия
            self.driver.execute_script("""
                var btn = document.querySelector('button[class*="modal__close"], [aria-label*="Закрыть"], .Modal_modal__close');
                if (btn) btn.click();
            """)

        # 3. Ждём исчезновения оверлея (точный класс из ошибки)
        try:
            WebDriverWait(self.driver, 15).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, '.Modal_modal_overlay__x2ZCr'))
            )
        except TimeoutException:
            # 4. Принудительное удаление оверлея и модалки
            self.driver.execute_script("""
                var overlay = document.querySelector('.Modal_modal_overlay__x2ZCr');
                if (overlay) {
                    overlay.style.display = 'none';
                    overlay.remove();
                }
                document.querySelectorAll('section[class*="modal"]').forEach(el => el.remove());
            """)
            time.sleep(2.5)  # пауза после удаления (важно для Firefox)

        # 5. Стабилизация интерфейса
        self.driver.execute_script("document.body.focus(); window.scrollTo(0, 0);")
        time.sleep(0.5)

        return order_number