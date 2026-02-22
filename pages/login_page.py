import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from locators import LoginPageLocators
from pages.base_page import BasePage
from urls import Url


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    @allure.step('Кликнуть на иконку Показать/Скрыть пароль')
    def hide_or_show_password(self):
        self.click_on_element(LoginPageLocators.SHOW_PASSWORD)

    @allure.step('Авторизоваться пользователем')
    def login_user(self, user_data):
        # Ожидание загрузки страницы логина
        self.wait_load_url(Url.LOGIN_PAGE)
        
        # Заполнение полей
        self.enter_text_in_element(LoginPageLocators.EMAIL_INPUT, user_data['email'])
        self.enter_text_in_element(LoginPageLocators.PASSWORD_INPUT, user_data['password'])
        
        # Отправка формы
        self.click_on_element(LoginPageLocators.SUBMIT_BUTTON)
        
        # Ожидание перехода на главную страницу
        self.wait_load_url(Url.MAIN_PAGE)

    @allure.step('Перейти на страницу восстановления пароля')
    def go_to_recovery_password(self):
        self.click_on_element(LoginPageLocators.RECOVERY_PASSWORD)

    @allure.step('Проверить, что клик "показать/скрыть" меняет тип поля на text')
    def check_active_password_field(self):
        """Проверяет смену типа поля с password на text после клика на иконку"""
        password_input = self.get_element(LoginPageLocators.PASSWORD_INPUT)
        current_type = password_input.get_attribute('type')
        return current_type == 'text'

    @allure.step('Проверить видимость формы авторизации')
    def check_visible_login_form(self):
        return self.check_is_visible_element(LoginPageLocators.LOGIN_FORM)
    
    @allure.step('Проверить, что поле пароля подсвечено / активно после клика "показать/скрыть"')
    def check_active_password_field(self):
        """Проверяет, что контейнер поля получил класс активности (подсветка)"""
        container = self.get_element(LoginPageLocators.PASSWORD_CONTAINER)
        classes = container.get_attribute("class") or ""
        
        # Вариант 1: проверяем класс (самый надёжный, если он есть)
        is_highlighted = "input_status_active" in classes
        
        # Вариант 2: резервный — проверяем, что тип инпута сменился на text
        password_input = self.get_element(LoginPageLocators.PASSWORD_INPUT)
        is_text_type = password_input.get_attribute('type') == 'text'
        
        # Можно комбинировать условия по ситуации
        return is_highlighted or is_text_type