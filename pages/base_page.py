import allure
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 20)  # базовый таймаут, можно переопределять

    def get_url(self):
        return self.driver.current_url

    def wait_load_url(self, url, timeout=20):
        """Ожидание загрузки указанного URL"""
        WebDriverWait(self.driver, timeout).until(EC.url_to_be(url))

    def get_element(self, locator):
        """Находит один элемент по локатору"""
        return self.driver.find_element(*locator)

    def get_elements(self, locator):
        """Находит список элементов по локатору"""
        return self.driver.find_elements(*locator)

    @allure.step("Drag and drop элемента в цель")
    def drag_and_drop(self, locator_from, locator_to):
        """Перетаскивание элемента с помощью JavaScript"""
        element_from = self.get_element(locator_from)
        element_to = self.get_element(locator_to)

        self.driver.execute_script("""
            var source = arguments[0];
            var target = arguments[1];
            var dt = new DataTransfer();

            var dragStart = new DragEvent('dragstart', {bubbles: true, cancelable: true, dataTransfer: dt});
            source.dispatchEvent(dragStart);

            var dragEnter = new DragEvent('dragenter', {bubbles: true, cancelable: true, dataTransfer: dt});
            target.dispatchEvent(dragEnter);

            var dragOver = new DragEvent('dragover', {bubbles: true, cancelable: true, dataTransfer: dt});
            target.dispatchEvent(dragOver);

            var drop = new DragEvent('drop', {bubbles: true, cancelable: true, dataTransfer: dt});
            target.dispatchEvent(drop);

            var dragEnd = new DragEvent('dragend', {bubbles: true, cancelable: true, dataTransfer: dt});
            source.dispatchEvent(dragEnd);
        """, element_from, element_to)

    def wait_element(self, locator, timeout=20):
        """Ожидание видимости элемента"""
        WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def wait_for_invisibility_of_element(self, locator, timeout=15, message=None):
        """Ожидание исчезновения элемента"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator),
                message=message or "Элемент не исчез"
            )
            return True
        except TimeoutException:
            return False

    def wait_show_text_in_element(self, locator, text, timeout=20):
        """Ожидание появления текста в элементе"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element(locator, text)
            )
            return True
        except TimeoutException:
            return False

    def js_click_on_element(self, locator):
        """Клик по элементу через JavaScript (обходит перекрытия)"""
        self.wait_element(locator)
        element = self.get_element(locator)
        self.driver.execute_script("arguments[0].click();", element)

    def click_on_element(self, locator):
        """Обычный клик по элементу с fallback на JS-клик"""
        self.wait_element(locator)
        element = self.get_element(locator)
        try:
            element.click()
        except:
            self.js_click_on_element(locator)

    def enter_text_in_element(self, locator, text):
        """Ввод текста в поле"""
        self.wait_element(locator)
        self.get_element(locator).send_keys(text)

    def get_value_from_element(self, locator):
        """Получение текста элемента"""
        self.wait_element(locator)
        return self.get_element(locator).text

    def get_attribute_from_element(self, locator, attribute):
        """Получение значения атрибута элемента"""
        self.wait_element(locator)
        return self.get_element(locator).get_attribute(attribute)

    def check_is_visible_element(self, locator, timeout=10):
        """Проверка видимости элемента"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    # ──────────────────────────────────────────────
    # Новые методы специально для устранения driver-вызовов
    # ──────────────────────────────────────────────

    def wait_for_invisibility_by_css(self, css_selector, timeout=15):
        """Ожидание исчезновения элемента по CSS-селектору"""
        return self.wait_for_invisibility_of_element(
            (By.CSS_SELECTOR, css_selector),
            timeout=timeout,
            message=f"Элемент по селектору '{css_selector}' не исчез"
        )

    def js_remove_element(self, css_selector):
        """Принудительное удаление элемента по CSS-селектору"""
        self.driver.execute_script(f"""
            var el = document.querySelector('{css_selector}');
            if (el) el.remove();
        """)

    def js_remove_all_modals_and_overlays(self):
        """Удалить все модальные окна и оверлеи"""
        self.driver.execute_script("""
            document.querySelectorAll(
                'section[class*="modal"], .Modal_modal_overlay__x2ZCr, [class*="overlay"]'
            ).forEach(el => el.remove());
        """)

    def js_click_by_css(self, css_selector):
        """JS-клик по элементу, найденному по CSS-селектору"""
        self.driver.execute_script(f"""
            var el = document.querySelector('{css_selector}');
            if (el) el.click();
        """)