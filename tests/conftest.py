
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from url import MAIN_PAGE_URL, LOGIN_URL
from locators.locators import LoginPageLocators
from data import Credentials
from url import *

class WebdriverFactory:
    @staticmethod
    def get_webdriver(browser_name):
        if browser_name == "firefox":
            return webdriver.Firefox()
        elif browser_name == "chrome":
            return webdriver.Chrome()
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

# Эта функция добавляет возможность передачи параметра --browser в командной строке pytest
def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        choices=["chrome", "firefox"],
        help="Выбор браузера: 'chrome' или 'firefox'."
    )

@pytest.fixture
def driver(request):
    # Получаем параметр браузера из командной строки
    browser_name = request.config.getoption("--browser")
    # Создаем и возвращаем соответствующий драйвер
    driver = WebdriverFactory.get_webdriver(browser_name)
    # Открываем главную страницу
    driver.get(MAIN_PAGE_URL)
    # Устанавливаем неявное ожидание
    driver.implicitly_wait(10)
    driver.maximize_window()  # Открытие окна на весь экран
    yield driver
    #Закрытие браузера
    driver.quit()


@pytest.fixture
def login_authorized_profile(driver):
    """
    Фикстура для авторизации пользователя.
    """
    driver.get(LOGIN_URL)#перейти на страницу с формой входа

    # Ожидаем загрузки страницы логина
    WebDriverWait(driver, 15).until(EC.presence_of_element_located(LoginPageLocators.LOGIN_TITLE))

    # Заполняем поля email и пароль
    email_field = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located(LoginPageLocators.EMAIL_FIELD)
    )
    email_field.send_keys(Credentials.email)
    
    password_field = driver.find_element(*LoginPageLocators.PASSWORD_FIELD)
    password_field.send_keys(Credentials.password)
    
    # Нажимаем кнопку входа
    login_button = driver.find_element(*LoginPageLocators.LOGIN_BUTTON)
    login_button.click()
    
    # Ожидаем редирект на главную страницу
    WebDriverWait(driver, 10).until(EC.url_to_be(MAIN_PAGE_URL))
    
    return driver