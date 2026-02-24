import allure
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
from urls import Url


class TestMainPage:

    @allure.title('Проверка перехода по клику на «Конструктор»')
    def test_go_to_main_page(self, driver):
        main_page = MainPage(driver)
        
        # Переходим в ленту заказов
        main_page.go_to_orders_feed_page()
        
        # Возвращаемся на главную через кнопку «Конструктор»
        order_feed_page = OrderFeedPage(driver)
        order_feed_page.go_to_main_page()
        
        # Проверяем, что URL соответствует главной странице
        assert main_page.get_url() == Url.MAIN_PAGE

    @allure.title('Проверка перехода по клику на «Лента заказов»')
    def test_go_to_orders_page(self, driver):
        main_page = MainPage(driver)
        
        # Переходим в ленту заказов
        main_page.go_to_orders_feed_page()
        
        # Проверяем корректный URL страницы ленты
        assert main_page.get_url() == Url.ORDERS_FEED_PAGE

    @allure.title('Проверка открытия окна с деталями ингредиента')
    def test_open_details_window(self, driver):
        main_page = MainPage(driver)
        
        # Открываем детали любого ингредиента
        main_page.view_ingredient()
        
        # Проверяем появление модального окна
        assert main_page.check_visible_ingredient_detail_windows()

    @allure.title('Проверка закрытия окна с деталями ингредиента')
    def test_close_details_window(self, driver):
        main_page = MainPage(driver)
        
        # Открываем детали ингредиента
        main_page.view_ingredient()
        
        # Закрываем модальное окно
        main_page.close_ingredient_detail_windows()
        
        # Проверяем, что окно больше не видно
        assert not main_page.check_visible_ingredient_detail_windows()

    @allure.title('Проверка увеличения счётчика ингредиента')
    def test_increment_ingredient_counter(self, driver):
        main_page = MainPage(driver)
        
        # Запоминаем начальное значение счётчика
        start_value = main_page.get_ingredient_count()
        
        # Добавляем ингредиент в корзину
        main_page.add_ingredient_in_basket()
        
        # Получаем новое значение счётчика
        finish_value = main_page.get_ingredient_count()
        
        # Проверяем, что счётчик увеличился
        assert int(start_value) < int(finish_value)

    @allure.title('Проверка оформления заказа авторизованным пользователем')
    def test_create_order_authorized_user(self, driver, login_user):
        main_page = MainPage(driver)
        
        # Создаём заказ (авторизация уже выполнена фикстурой)
        order = main_page.create_order()
        
        # Проверяем, что номер заказа успешно получен
        assert order, "Номер заказа не получен"