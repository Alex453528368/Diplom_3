import allure
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
from pages.profile_page import ProfilePage


class TestOrders:

    @allure.title('Проверка открытия деталей заказа')
    def test_open_order_detail_window(self, driver):
        main_page = MainPage(driver)
        
        # Переходим в ленту заказов
        main_page.go_to_orders_feed_page()
        
        # Открываем любой заказ
        order_feed_page = OrderFeedPage(driver)
        order_feed_page.open_order()
        
        # Проверяем появление модального окна с деталями
        assert order_feed_page.check_visible_order_window(), \
            "Модальное окно с деталями заказа не открылось"

    @allure.title('Проверка отображения заказов пользователя в личной истории')
    def test_orders_in_orders_history_is_on_order_feed_page(self, driver, login_user):
        main_page = MainPage(driver)
        
        # Создаём заказ и получаем его номер
        created_order_number = main_page.create_order()
        
        # Убеждаемся, что номер реальный (не заглушка)
        assert created_order_number != '9999' and created_order_number.isdigit() and len(created_order_number) > 3, \
            f"Создан фейковый заказ #{created_order_number}"
        
        # Переходим в профиль → историю заказов
        main_page.go_to_profile()
        profile_page = ProfilePage(driver)
        
        # Получаем список заказов из истории
        user_orders = profile_page.get_history_orders()
        
        # Проверяем наличие созданного заказа в истории
        assert created_order_number in user_orders, \
            f"Заказ #{created_order_number} не найден в истории. Видим: {user_orders}"

    @allure.title('Проверка увеличения счётчика «Выполнено за всё время»')
    def test_check_all_orders_increment(self, driver, login_user):
        main_page = MainPage(driver)
        main_page.go_to_orders_feed_page()
        
        order_feed_page = OrderFeedPage(driver)
        
        # Запоминаем текущее значение счётчика за всё время
        all_before_str = order_feed_page.get_all_orders_count()
        all_before = int(all_before_str.replace(' ', '').replace(',', ''))
        
        # Возвращаемся на главную и создаём заказ
        order_feed_page.go_to_main_page()
        main_page.create_order()
        
        # Возвращаемся в ленту и проверяем новый счётчик
        main_page.go_to_orders_feed_page()
        order_feed_page = OrderFeedPage(driver)
        all_after_str = order_feed_page.get_all_orders_count()
        all_after = int(all_after_str.replace(' ', '').replace(',', ''))
        
        assert all_after >= all_before + 1, \
            f"Счётчик 'за всё время' не увеличился: {all_before_str} → {all_after_str}"

    @allure.title('Проверка увеличения счётчика «Выполнено за сегодня»')
    def test_check_today_orders_increment(self, driver, login_user):
        main_page = MainPage(driver)
        main_page.go_to_orders_feed_page()
        
        order_feed_page = OrderFeedPage(driver)
        
        # Запоминаем текущее значение счётчика за сегодня
        today_before_str = order_feed_page.get_today_orders_count()
        today_before = int(today_before_str.replace(' ', '').replace(',', ''))
        
        # Создаём заказ
        order_feed_page.go_to_main_page()
        main_page.create_order()
        
        # Возвращаемся в ленту и проверяем обновление
        main_page.go_to_orders_feed_page()
        order_feed_page = OrderFeedPage(driver)
        today_after_str = order_feed_page.get_today_orders_count()
        today_after = int(today_after_str.replace(' ', '').replace(',', ''))
        
        assert today_after >= today_before + 1, \
            f"Счётчик 'за сегодня' не увеличился: {today_before_str} → {today_after_str}"

    @allure.title('Проверка появления заказа в разделе «В работе»')
    def test_order_number_is_order_in_work(self, driver, login_user):
        main_page = MainPage(driver)
        
        # Создаём заказ и получаем номер
        created_order_number = main_page.create_order()
        
        # Переходим в ленту заказов
        main_page.go_to_orders_feed_page()
        order_feed_page = OrderFeedPage(driver)
        
        # Проверяем появление заказа в разделе «В работе»
        assert order_feed_page.check_order_in_work(created_order_number), \
            f"Заказ #{created_order_number} не появился в разделе 'В работе'"