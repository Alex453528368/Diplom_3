import allure
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from locators import OrdersPageLocators
from pages.base_page import BasePage
from urls import Url


class OrderFeedPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    @allure.step('Перейти на главную страницу')
    def go_to_main_page(self):
        # Клик по кнопке «Конструктор» и ожидание загрузки главной
        self.click_on_element(OrdersPageLocators.GO_TO_CONSTRUCTOR_BTN)
        self.wait_load_url(Url.MAIN_PAGE)

    @allure.step('Открыть детали любого заказа')
    def open_order(self):
        # Клик по первому элементу в списке заказов
        self.click_on_element(OrdersPageLocators.ORDER_ITEM)

    @allure.step('Получить список номеров заказов')
    def get_history_orders(self):
        # Ожидание появления списка заказов и извлечение номеров (без # и ведущих нулей)
        self.wait_element(OrdersPageLocators.ALL_ORDERS_LIST)
        orders = [element.text.lstrip('#0') for element in self.get_elements(OrdersPageLocators.ALL_ORDERS_LIST)]
        return orders

    @allure.step('Получить счётчик «Выполнено за всё время»')
    def get_all_orders_count(self):
        return self.get_value_from_element(OrdersPageLocators.ALL_ORDERS_COUNT)

    @allure.step('Получить счётчик «Выполнено за сегодня»')
    def get_today_orders_count(self):
        return self.get_value_from_element(OrdersPageLocators.TODAY_ORDERS_COUNT)

    @allure.step('Проверить появление заказа в разделе «В работе»')
    def check_order_in_work(self, order):
        # Ожидание появления номера заказа в блоке «В работе»
        return self.wait_show_text_in_element(OrdersPageLocators.ORDER_IN_WORK, order)

    @allure.step('Проверить видимость модального окна с деталями заказа')
    def check_visible_order_window(self):
        # Проверка, что модалка деталей заказа отображается
        return self.check_is_visible_element(OrdersPageLocators.MODAL_WINDOW)