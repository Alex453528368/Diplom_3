import allure
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.profile_page import ProfilePage


class TestProfilePage:

    @allure.title('Проверка перехода по клику на «Личный кабинет»')
    def test_go_to_user_profile(self, driver, login_user):
        main_page = MainPage(driver)
        
        # Переходим в личный кабинет
        main_page.go_to_profile()
        
        # Проверяем, что информация профиля отображается
        profile_page = ProfilePage(driver)
        assert profile_page.check_visible_profile_info()

    @allure.title('Проверка перехода в раздел «История заказов»')
    def test_go_to_story_order(self, driver, login_user):
        main_page = MainPage(driver)
        
        # Создаём заказ (чтобы была история)
        main_page.create_order()
        
        # Переходим в личный кабинет
        main_page.go_to_profile()
        
        # Открываем историю заказов
        profile_page = ProfilePage(driver)
        profile_page.go_to_orders_history()
        
        # Проверяем видимость блока с историей заказов
        assert profile_page.check_visible_order_history()

    @allure.title('Проверка выхода из аккаунта')
    def test_exit_from_profile(self, driver, login_user):
        main_page = MainPage(driver)
        
        # Переходим в личный кабинет
        main_page.go_to_profile()
        
        # Выходим из аккаунта
        profile_page = ProfilePage(driver)
        profile_page.logout()
        
        # Проверяем возврат на страницу входа
        login_page = LoginPage(driver)
        assert login_page.check_visible_login_form()