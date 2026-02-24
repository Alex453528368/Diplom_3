class HeaderLocators:
    GO_TO_CONSTRUCTOR_BTN = ('xpath', '//p[text()="Конструктор"]')  # кнопка перехода на главную страницу
    GO_TO_ORDERS_FEED_BTN = ('xpath', '//p[text()="Лента Заказов"]')  # кнопка перехода в ленту заказов


class OrdersPageLocators(HeaderLocators):
    ORDER_ITEM = ('xpath', '//li[contains(@class, "OrderHistory_listItem")]')  # заказ
    ALL_ORDERS_COUNT = ('xpath', '//p[text()="Выполнено за все время:"]/../p[contains(@class, "OrderFeed_number")]')  # счетчик всех заказов
    TODAY_ORDERS_COUNT = ('xpath', '//p[text()="Выполнено за сегодня:"]/../p[contains(@class, "OrderFeed_number")]')  # счетчик заказов за сегодня
    ALL_ORDERS_LIST = ('xpath', '//p[contains(text(), "#")]')  # лента выполненных заказов
    ORDER_IN_WORK = ('xpath', '//ul[contains(@class, "orderListReady")]/li')  # заказ в работе
    MODAL_WINDOW = ('xpath', '//section[contains (@class, "modal_opened")]')  # модальное окно


class MainPageLocators(HeaderLocators):
    ENTER_IN_ACCOUNT = ('xpath', '//button[text()="Войти в аккаунт"]')  # кнопка Войти в аккаунт
    BASKET_AREA = ('xpath', '//ul[contains(@class, "BurgerConstructor_basket")]')  # область сборки бургера
    CREATE_ORDER = ('xpath', '//button[text()="Оформить заказ"]')  # кнопка Оформить заказ
    INGREDIENT = ('xpath', '//a[contains(@class,"BurgerIngredient")]')  # ингредиент бургера
    INGREDIENT_COUNTER = ('xpath', '//p[contains(@class, "counter__num")]')  # счетчик ингредиента
    ORDER_NUMBER = ('xpath', '//h2[contains(@class, "Modal_modal__title_shadow")]')  # номер заказа
    GO_TO_PROFILE_BTN = ('xpath', '//p[text()="Личный Кабинет"]')  # кнопка перехода в личный кабинет
    MODAL_WINDOW = ('xpath', '//section[contains (@class, "modal_opened")]')  # модальное окно
    CLOSE_MODAL_WINDOW = ('xpath', '//button[contains(@class, "modal__close")]')  # кнопка закрытия модального окна


class LoginPageLocators(HeaderLocators):
    LOGIN_FORM = ('xpath', '//h2[text()="Вход"]')  # форма авторизации
    EMAIL_INPUT = ('xpath', '//label[text()="Email"]/../input')  # поле ввода электронной почты
    PASSWORD_INPUT = ('xpath', '//label[text()="Пароль"]/../input')  # поле ввода пароля
    SUBMIT_BUTTON = ('xpath', '//form//button')  # кнопка Войти
    RECOVERY_PASSWORD = ('xpath', '//a[text()="Восстановить пароль"]')  # кнопка Восстановить пароль
    SHOW_PASSWORD = ('xpath', '//div[contains(@class, "input__icon-action")]')  # кнопка Показать/скрыть пароль
    PASSWORD_CONTAINER = ('xpath', '//label[text()="Пароль"]/..')  # отображение активности поля


class RecoveryPageLocators(HeaderLocators):
    RECOVERY_FORM = ('xpath', '//h2[text()="Восстановление пароля"]')  # форма восстановления пароля
    EMAIL_INPUT = ('xpath', '//label[text()="Email"]/../input')  # поле ввода электронной почты
    SUBMIT_BUTTON = ('xpath', '//form//button')  # кнопка Восстановить
    INFO_ABOUT_RECOVERY_CODE = ('xpath', '//label[text()="Введите код из письма"]')  # сообщение о восстановлении


class ProfilePageLocators(HeaderLocators):
    PROFILE_INFO = ('xpath', '//div[contains(@class, "Profile")]')  # информация о профиле пользователя
    ORDER_HISTORY_BTN = ('xpath', '//a[text()="История заказов"]')  # кнопка перехода в историю заказов
    EXIT_BTN = ('xpath', '//button[text()="Выход"]')  # кнопка Выйти из профиля
    ORDERS_HISTORY_LIST = ('xpath', '//p[contains(text(), "#")]')  # история заказов пользователя
