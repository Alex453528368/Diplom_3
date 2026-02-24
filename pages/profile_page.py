import allure
from locators import ProfilePageLocators
from pages.base_page import BasePage
from urls import Url


class ProfilePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    @allure.step('Перейти в историю заказов')
    def go_to_orders_history(self):
        # Клик по ссылке «История заказов»
        self.click_on_element(ProfilePageLocators.ORDER_HISTORY_BTN)

    @allure.step('Перейти в ленту заказов')
    def go_to_orders_feed_page(self):
        # Клик по кнопке «Лента Заказов» и ожидание загрузки страницы
        self.click_on_element(ProfilePageLocators.GO_TO_ORDERS_FEED_BTN)
        self.wait_load_url(Url.ORDERS_FEED_PAGE)

    @allure.step('Выйти из аккаунта')
    def logout(self):
        # Клик по кнопке «Выход»
        self.click_on_element(ProfilePageLocators.EXIT_BTN)

    @allure.step('Получить список номеров заказов из истории')
    def get_history_orders(self):
        # Переход в историю → ожидание списка → извлечение номеров (без # и ведущих нулей)
        self.go_to_orders_history()
        self.wait_element(ProfilePageLocators.ORDERS_HISTORY_LIST)
        orders = [element.text.lstrip('#0') for element in self.get_elements(ProfilePageLocators.ORDERS_HISTORY_LIST)]
        return orders

    @allure.step('Проверить видимость блока информации о профиле')
    def check_visible_profile_info(self):
        # Проверка, что информация профиля отображается
        return self.check_is_visible_element(ProfilePageLocators.PROFILE_INFO)

    @allure.step('Проверить видимость списка истории заказов')
    def check_visible_order_history(self):
        # Проверка, что блок истории заказов виден
        return self.check_is_visible_element(ProfilePageLocators.ORDERS_HISTORY_LIST)