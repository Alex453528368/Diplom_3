import allure
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
        self.js_click_on_element(MainPageLocators.CLOSE_MODAL_WINDOW)

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
        self.wait_element(MainPageLocators.INGREDIENT)
        self.wait_element(MainPageLocators.BASKET_AREA)

        self.drag_and_drop(
            MainPageLocators.INGREDIENT,
            MainPageLocators.BASKET_AREA
        )

        # Ждём, пока хотя бы один счётчик ингредиента станет больше 0
        self.wait.until(
            lambda _: any(
                int(el.text.strip() or '0') > 0
                for el in self.get_elements(MainPageLocators.INGREDIENT_COUNTER)
            ),
            message="После drag-and-drop ни один счётчик ингредиента не увеличился"
        )

    @allure.step('Нажать кнопку Войти в аккаунт')
    def enter_in_account(self):
        self.click_on_element(MainPageLocators.ENTER_IN_ACCOUNT)

    @allure.step('Создать заказ')
    def create_order(self):
        # добавляем хотя бы минимальный набор ингредиентов
        self.add_ingredient_in_basket()

        # ждём, пока кнопка станет активной
        self.wait.until(
            EC.element_to_be_clickable(MainPageLocators.CREATE_ORDER)
        )

        self.click_on_element(MainPageLocators.CREATE_ORDER)

        # ждём появления модального окна
        self.wait.until(
            EC.visibility_of_element_located(MainPageLocators.ORDER_NUMBER)
        )

        # ждём, пока текст перестанет быть "9999"
        self.wait.until(
            lambda _: not self._is_placeholder_order_number(),
            message="Номер заказа остался 9999 после 45 секунд"
        )

        # получаем уже настоящий номер
        order_text = self.get_value_from_element(MainPageLocators.ORDER_NUMBER)
        order_number = order_text.replace('#', '').lstrip('0').strip()

        # закрываем модалку через JS-клик (надёжнее)
        self.js_click_by_css('button[class*="Modal_modal__close"]')

        # ждём исчезновения оверлея и модалки
        self.wait_for_invisibility_by_css('.Modal_modal_overlay__x2ZCr', timeout=10)
        self.wait_for_invisibility_of_element(MainPageLocators.MODAL_WINDOW, timeout=10)

        return order_number

    def _is_placeholder_order_number(self):
        """Вспомогательный метод: проверяет, что номер всё ещё заглушка"""
        try:
            text = self.get_value_from_element(MainPageLocators.ORDER_NUMBER)
            cleaned = text.replace('#', '').replace(' ', '').lstrip('0')
            return cleaned in ('9999', '999', '') or not cleaned.isdigit()
        except:
            return True