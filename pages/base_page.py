
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from locators.locators import MainPageLocators

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    #Возвращает текущий URL страницы"
    def current_url(self):
        return self.driver.current_url

    #Поиск элемента с ожиданием
    def find_element_with_wait(self, locator):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(locator)
        )
        return self.driver.find_element(*locator)

    
    def wait_for_element_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
    
    #Клик по элементу
    def click_to_element(self, locator, timeout=10):
        element = self.wait_for_element_clickable(locator, timeout)
        element.click()

   #Ожидание видимости элемента"
    def wait_for_visible(self, locator, timeout=15):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def wait_for_invisible(self, locator, timeout=15):
        return WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))

    # Ожидание исчезновения оверлея
    def wait_for_overlay_to_disappear(self, timeout=15):
        """Ожидает исчезновения оверлея модального окна"""
        return self.wait_for_invisible(MainPageLocators.MODAL_OVERLAY, timeout)

        #Получение текста элемента
    def get_text_from_element(self, locator):
        return self.find_element_with_wait(locator).text

    
    #Проверка видимости элемента
    def is_element_displayed(self, locator):
        try:
            element = self.find_element_with_wait(locator)
            return element.is_displayed()
        except TimeoutException:
            return False
    

    
    #Перетаскивание элемента   
    def drag_and_drop(self, source_locator, target_locator):
        """
        Перетаскивает элемент из source_locator в target_locator с использованием ActionChains.
        :param source_locator: Локатор элемента, который нужно перетащить.
        :param target_locator: Локатор элемента, куда нужно перетащить.
        """
        source_element = self.wait_for_visible(source_locator)
        target_element = self.wait_for_visible(target_locator)
        
        actions = ActionChains(self.driver)
        actions.drag_and_drop(source_element, target_element).perform()

    #Ожидание
    def wait(self, seconds):
        import time
        time.sleep(seconds)


    