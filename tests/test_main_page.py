import allure
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage

from url import *
import time

@allure.feature('Основной функционал')

class TestMainPage:

    @allure.title('Переход по клику на «Конструктор»')
    def test_click_constructor(self, driver):
        main_page = MainPage(driver)
        
        with allure.step('Нажимаем на "Конструктор"'):
            main_page.click_constructor()

        with allure.step('Проверяем, что находимся на странице конструктора'):
            assert main_page.current_url() == MAIN_PAGE_URL
            
        with allure.step('Проверяем, что секция "Собери бургер" отображается'):
            assert main_page.is_burger_constructor_visible(), "Секция 'Собери бургер' не отображается!"

        

    @allure.title('Переход по клику на раздел «Лента заказов»')
    def test_click_feed_order(self, driver):
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)

        with allure.step('Нажимаем на "Лента заказов"'):
            main_page.click_order_feed()

        with allure.step('Проверяем, что находимся на странице "Лента заказов"'):
            assert main_page.current_url() == ORDER_FEED_URL

        with allure.step('Проверяем, что секция "Лента заказов" отображается'):
            assert order_feed_page.is_order_feed_visible(), "Секция 'Лента заказов' не отображается!"

    
    @allure.title('При клике на ингредиент, появляется всплывающее окно с деталями ингредиента')
    def test_click_bun_modal_appears(self, driver):
        main_page = MainPage(driver)
        
        with allure.step('Кликаем на ингредиент Булка'):
            main_page.click_ingredient_bun()

        with allure.step('Проверяем, что отображается модальное окно с информацией об ингредиенте'):
            assert main_page.is_ingredient_details_visible(), "Окно 'Детали ингредиента' не отображается!"



    @allure.title('Закрытие модального окнас с деталями ингредиента кликом по крестику')
    def test_close_modal_by_cross(self, driver):
        main_page = MainPage(driver)
        
        with allure.step('Кликаем на ингредиент Булка'):
            main_page.click_ingredient_bun()

        with allure.step('Проверяем, что отображается модальное окно с информацией об ингредиенте'):
            assert main_page.is_ingredient_details_visible()
            
        with allure.step('Кликаем на крестик в модльном окне'):
            main_page.close_ingredient_details()

        time.sleep(0.5)

        with allure.step('Проверяем, что модальное окно не отображается'):
            assert not main_page.is_ingredient_details_visible()


    @allure.title('При добавлении булки в заказ счётчик булки увеличивается')
    def test_bun_counter_increases_when_added_to_order(self, driver):
        main_page = MainPage(driver)
        inital_counter = main_page.get_bun_counter()

        with allure.step('Перетаскиваем Булку на конструктор заказа'):
            main_page.drag_and_drop_bun_to_constructor()

        with allure.step('Получение значения счётчика булки'):
            new_counter = main_page.get_bun_counter()

        with allure.step('Сравниваем количество до и после добавления булок в заказ'):
            assert new_counter > inital_counter