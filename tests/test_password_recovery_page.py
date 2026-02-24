import allure
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.recovery_page import RecoveryPage


class TestPasswordRecovery:

    @allure.title('Проверка перехода на страницу восстановления пароля')
    def test_go_to_password_recovery_page(self, driver):
        main_page = MainPage(driver)
        
        # Переходим на страницу входа
        main_page.go_to_login()
        
        # Кликаем по ссылке «Восстановить пароль»
        login_page = LoginPage(driver)
        login_page.go_to_recovery_password()
        
        # Проверяем, что открылась форма восстановления
        recovery_page = RecoveryPage(driver)
        assert recovery_page.check_visible_recovery_form()

    @allure.title('Проверка отправки формы восстановления пароля')
    def test_recovery_password_form(self, driver, user_data):
        main_page = MainPage(driver)
        
        # Переходим на страницу входа
        main_page.go_to_login()
        
        # Переходим на восстановление пароля
        login_page = LoginPage(driver)
        login_page.go_to_recovery_password()
        
        # Заполняем email и отправляем форму
        recovery_page = RecoveryPage(driver)
        recovery_page.filling_recovery_form(user_data['user'])
        
        # Проверяем появление поля для ввода кода из письма
        assert recovery_page.check_visible_recovery_code()

    @allure.title('Проверка активности поля пароля после клика «показать/скрыть»')
    def test_check_activities_input_password(self, driver):
        main_page = MainPage(driver)
        
        # Переходим на страницу входа
        main_page.go_to_login()
        
        # Кликаем по иконке показать/скрыть пароль
        login_page = LoginPage(driver)
        login_page.hide_or_show_password()
        
        # Проверяем, что поле пароля стало активным
        assert login_page.check_active_password_field(), \
            "Поле пароля не стало активным после клика на иконку"