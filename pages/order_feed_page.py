import allure
import re
import requests
from pages.base_page import BasePage
from locators.locators import *
from url import API_INGREDIENTS, API_ORDERS
import time


class OrderFeedPage(BasePage):
        
    @allure.step("Cекция 'Лента заказов' отображается")
    def is_order_feed_visible(self):
        return self.find_element_with_wait(OrderFeedLocators.ORDER_FEED_HEADER).is_displayed()
       
    @allure.step("Получение счётчика 'Выполнено за всё время'")
    def get_total_orders_count(self):
        element = self.wait_for_visible(OrderFeedLocators.TOTAL_ORDERS_COUNTER)
        return element.text
    
    @allure.step("Получение счётчика 'Выполнено за сегодня'")
    def get_today_orders_count(self):
        element = self.wait_for_visible(OrderFeedLocators.TODAY_ORDERS_COUNTER)
        return element.text
    
        
    @allure.step("Получение всех номеров заказов в работе")
    def get_all_orders_in_work(self):
        """Получает список всех номеров заказов в разделе 'В работе'"""
        try:
            self.wait_for_visible(OrderFeedLocators.ORDER_NUMBER_IN_WORK, timeout=10)
        except:
            pass
        
        elements = self.driver.find_elements(*OrderFeedLocators.ORDER_NUMBER_IN_WORK)
        
        orders = []
        for el in elements:
            text = el.text.strip()
            if text and text != 'Все текущие заказы готовы!':
                # Извлекаем цифры из текста
                numbers = re.findall(r'\d+', text)
                if numbers:
                    # Берём первое найденное число
                    orders.append(numbers[0])
        
        print(f"\nНайдено заказов в работе: {len(orders)}")
        print(f"Список заказов: {orders}")
        
        return orders

    @allure.step("Ожидание обновления счётчика 'Выполнено за всё время'")
    def wait_for_total_counter_update(self, initial_value, timeout=30):
        start_time = time.time()
        while time.time() - start_time < timeout:
            current_value = self.get_total_orders_count()
            if current_value > initial_value:
                return True
            time.sleep(1)
        return False

    @allure.step("Ожидание обновления счётчика 'Выполнено за сегодня'")
    def wait_for_today_counter_update(self, initial_value, timeout=30):
        start_time = time.time()
        while time.time() - start_time < timeout:
            current_value = self.get_today_orders_count()
            if current_value > initial_value:
                return True
            time.sleep(1)
        return False
    
    @allure.step("Ожидание появления номера заказа в разделе 'В работе'")
    def wait_for_order_in_work(self, order_number, timeout=30):
        start_time = time.time()
        while time.time() - start_time < timeout:
            orders = self.get_all_orders_in_work()
            
            for order in orders:
                if int(order) == int(order_number):
                    return True
            time.sleep(2)
        return False

    #Создание заказа
    @allure.step("Получение списка ингредиентов через API")
    def get_ingredients_via_api(self):
        """Получает список всех ингредиентов через API"""
        response = requests.get(API_INGREDIENTS, timeout=10)
        response.raise_for_status()
        ingredients = response.json().get('data', [])
        return ingredients
    
    @allure.step("Получение ID ингредиента для заказа")
    def get_ingredient_ids_for_order(self, ingredient_type="bun"):
        """Получает ID ингредиента для создания заказа"""
        ingredients = self.get_ingredients_via_api()
        
        if ingredient_type == "bun":
            # Ищем булку
            for ingredient in ingredients:
                if ingredient.get('type') == 'bun':
                    return [ingredient.get('_id')]
        else:
            # Ищем соус или начинку
            for ingredient in ingredients:
                if ingredient.get('type') == ingredient_type:
                    return [ingredient.get('_id')]
        return []
    
    @allure.step("Получение полного списка ID ингредиентов для бургера")
    def get_full_burger_ingredients(self):
        """Получает ID ингредиентов для полного бургера (булка + соус + начинка)"""
        ingredients = self.get_ingredients_via_api()
        
        bun_id = None
        sauce_id = None
        main_id = None
        
        for ingredient in ingredients:
            ingredient_type = ingredient.get('type')
            if ingredient_type == 'bun' and not bun_id:
                bun_id = ingredient.get('_id')
            elif ingredient_type == 'sauce' and not sauce_id:
                sauce_id = ingredient.get('_id')
            elif ingredient_type == 'main' and not main_id:
                main_id = ingredient.get('_id')
        
        # Возвращаем список ID для заказа (булка, соус, начинка)
        return [bun_id, sauce_id, main_id]
    
    @allure.step("Создание заказа через API")
    def create_order_via_api(self, ingredients_ids, access_token=None):
        """Создаёт заказ через API"""
        headers = {'Content-Type': 'application/json'}
        if access_token:
            headers['Authorization'] = access_token
        
        data = {'ingredients': ingredients_ids}
        
        response = requests.post(
            API_ORDERS,
            headers=headers,
            json=data,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    
    
    @allure.step("Получение номера заказа через API с авторизацией")
    def get_order_number_via_api_with_auth(self, access_token):
        """Создаёт заказ через API с токеном авторизации"""
        ingredients_ids = self.get_full_burger_ingredients()
        order_response = self.create_order_via_api(ingredients_ids, access_token)
        order_number = order_response.get('order', {}).get('number')
        return order_number