from selenium.webdriver.common.by import By

class MainPageLocators:
    # Шапка сайта (навигация)
    CONSTRUCTOR_BUTTON = (By.XPATH, "//p[contains(@class, 'AppHeader_header__linkText') and text()='Конструктор']")
    ORDER_FEED_BUTTON = (By.XPATH, "//p[contains(@class, 'AppHeader_header__linkText') and text()='Лента Заказов']")
    
    
    # Секция конструктора
    BURGER_CONSTRUCTOR_SECTION = (By.XPATH, "//section[contains(@class, 'BurgerIngredients_ingredients')]")
    
    # Ингредиенты
    INGREDIENT_BUN_R2D3 = (By.XPATH, "//img[@alt='Флюоресцентная булка R2-D3']")
    
    # Цели для перетаскивания
    ORDER_TARGET_TOP = (By.XPATH, "//span[text()='Перетяните булочку сюда (верх)']/ancestor::div[contains(@class, 'constructor-element')]")
    ORDER_TARGET_BOTTOM = (By.XPATH, "//span[text()='Перетяните булочку сюда (низ)']/ancestor::div[contains(@class, 'constructor-element')]")
    CONSTRUCTOR_CENTER = (By.XPATH, "//ul[contains(@class, 'BurgerConstructor_burger-list')]")
    
    # Модальное окно с деталями ингредиента
    INGREDIENT_DETAILS_MODAL = (By.XPATH, "//div[contains(@class, 'Modal_modal__content')]")
    CLOSE_MODAL_BUTTON = (By.XPATH, "//button[contains(@class, 'Modal_modal__close')]")
    
    # Счётчик ингредиента (исправленный)
    BUN_R2D3_COUNTER = (By.XPATH, "//img[@alt='Флюоресцентная булка R2-D3']/parent::a//p[contains(@class, 'counter')]")
    
    # Кнопка оформления заказа
    ORDER_BUTTON = (By.XPATH, "//button[text()='Оформить заказ']")
    
    ORDER_MODAL = (By.CSS_SELECTOR, "[class*='Modal_modal__container']")
    ORDER_NUMBER_MODAL = (By.CSS_SELECTOR, "[class*='Modal_modal__title']")
    CLOSE_MODAL_ORDER = (By.CSS_SELECTOR, "[class*='Modal_modal__close']")
    MODAL_OVERLAY = (By.CLASS_NAME, "Modal_modal_overlay__x2ZCr")

class OrderFeedLocators:
    #Заголовок страницы Лента заказов
    ORDER_FEED_HEADER = (By.XPATH, "//h1[text()='Лента заказов']")
    
    # Счётчики
    TOTAL_ORDERS_COUNTER = (By.XPATH, "//div[p[text()='Выполнено за все время:']]//p[contains(@class, 'OrderFeed_number__')]")
    TODAY_ORDERS_COUNTER = (By.XPATH, "//div[p[text()='Выполнено за сегодня:']]//p[contains(@class, 'OrderFeed_number__')]")
    
    # Номер заказа в работе
    ORDER_NUMBER_IN_WORK = (By.XPATH, "//ul[contains(@class, 'OrderFeed_orderListReady')]/li")
class LoginPageLocators:

    #Локаторы для входа
    LOGIN_TITLE = (By.XPATH, "//h2[text()='Вход']")
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти']") #кнопка "Войти"
    EMAIL_FIELD = (By.XPATH, "//div[.//label[text()='Email']]//input") #Поле Email
    PASSWORD_FIELD = (By.XPATH, "//input[@name='Пароль']") #Поле Пароль