import allure
from locators import RecoveryPageLocators
from pages.base_page import BasePage


class RecoveryPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    @allure.step('Заполнить форму восстановления пароля')
    def filling_recovery_form(self, user_data):
        self.enter_text_in_element(RecoveryPageLocators.EMAIL_INPUT, user_data['email'])
        self.click_on_element(RecoveryPageLocators.SUBMIT_BUTTON)

    @allure.step('Проверить видимость формы восстановления пароля')
    def check_visible_recovery_form(self):
        return self.check_is_visible_element(RecoveryPageLocators.RECOVERY_FORM)

    @allure.step('Проверить видимость запроса ввода кода подтверждения')
    def check_visible_recovery_code(self):
        return self.check_is_visible_element(RecoveryPageLocators.INFO_ABOUT_RECOVERY_CODE)