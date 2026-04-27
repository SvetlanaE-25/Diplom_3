import allure
from pages.base_page import BasePage
from locators.locators import MainPageLocators

class AccountPage(BasePage):

    @allure.step("Переход в Личный кабинет для входа")
    def open_login_page(self):
        self.click_to_element(MainPageLocators.ACCOUNT_PROFILE_BUTTON)