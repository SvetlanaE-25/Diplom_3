
import allure
from pages.base_page import BasePage
from locators.locators import MainPageLocators
from selenium.webdriver.common.action_chains import ActionChains
import time

class MainPage(BasePage):

    @allure.step("Клик на кнопку Конструктор")
    def click_constructor(self):
        self.click_to_element(MainPageLocators.CONSTRUCTOR_BUTTON)
    
    @allure.step("Клик на кнопку Лента заказов")
    def click_order_feed(self):
        self.click_to_element(MainPageLocators.ORDER_FEED_BUTTON)
    
    @allure.step("Клик на ингредиент Булка R2-D3")
    def click_ingredient_bun(self):
        self.click_to_element(MainPageLocators.INGREDIENT_BUN_R2D3)
    
    @allure.step("Проверка видимости модального окна с деталями ингредиента")
    def is_ingredient_details_visible(self):
        return self.is_element_displayed(MainPageLocators.INGREDIENT_DETAILS_MODAL)
    
    @allure.step("Закрытие модального окна с деталями ингредиента")
    def close_ingredient_details(self):
        self.click_to_element(MainPageLocators.CLOSE_MODAL_BUTTON)
    
    
    @allure.step("Перетаскивание булки в конструктор")
    def drag_and_drop_bun_to_constructor(self):
        ingredient_locator = MainPageLocators.INGREDIENT_BUN_R2D3
        target_locator = MainPageLocators.ORDER_TARGET_BOTTOM
        self.drag_and_drop(ingredient_locator, target_locator)
   

    @allure.step("Получение значения счётчика булки")
    def get_bun_counter(self):
        try:
            return int(self.get_text_from_element(MainPageLocators.BUN_R2D3_COUNTER))
        except:
            return 0
    
    @allure.step("Клик на кнопку Оформить заказ")
    def click_order_button(self):
        self.click_to_element(MainPageLocators.ORDER_BUTTON)

       
    @allure.step("Проверка видимости секции конструктора")
    def is_burger_constructor_visible(self):
        return self.is_element_displayed(MainPageLocators.BURGER_CONSTRUCTOR_SECTION)
    
    @allure.step("Ожидание появления модального окна с заказом")
    def wait_for_order_modal(self):
        self.wait_for_visible(MainPageLocators.ORDER_NUMBER_MODAL, timeout=30)

    @allure.step("Получение номера заказа из модального окна")
    def get_order_number_from_modal(self):
        element = self.find_element_with_wait(MainPageLocators.ORDER_NUMBER_MODAL)
        return element.text
    

    @allure.step("Закрытие модального окна с номером заказа")
    def close_order_details_modal(self):
        # Находим и удаляем оверлей
        element_to_remove = self.driver.find_element(*MainPageLocators.MODAL_OVERLAY)
        self.driver.execute_script("arguments[0].remove();", element_to_remove)
                
        # Ждём появления кнопки закрытия
        close_button = self.wait_for_visible(MainPageLocators.CLOSE_MODAL_ORDER, timeout=10)
        
        # Используем ActionChains для клика (обходит перекрытие)
        actions = ActionChains(self.driver)
        actions.move_to_element(close_button).click().perform()
        
    @allure.step("Получение токена авторизации из localStorage")
    def get_access_token(self):
        return self.driver.execute_script("return localStorage.getItem('accessToken');")

    