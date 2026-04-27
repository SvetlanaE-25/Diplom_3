import allure
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
import time
from url import *

@allure.feature('Оформление заказа')

class TestOrderFeedPage:

    @allure.title('При создании нового заказа счётчик "Выполнено за все время" увеличивается')
    def test_total_orders_counter_increases(self, login_authorized_profile):
        driver = login_authorized_profile
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)
        
        with allure.step('Переходим в ленту заказов и получаем начальное значение счётчика'):
            main_page.click_order_feed()
            initial_total = order_feed_page.get_total_orders_count()
            allure.attach(f"Начальное значение: {initial_total}", name="initial_total",
                         attachment_type=allure.attachment_type.TEXT)
        
        with allure.step('Создаём заказ через API и получаем номер заказа'):
            access_token = main_page.get_access_token()            
            order_number = order_feed_page.get_order_number_via_api_with_auth(access_token)
            allure.attach(f"Номер заказа: {order_number}", name="order_number",
                        attachment_type=allure.attachment_type.TEXT)
        
        with allure.step('Ожидаем обновления счётчика в ленте заказов'):
            # Ждём, пока счётчик увеличится
            counter_updated = order_feed_page.wait_for_total_counter_update(initial_total)
            assert counter_updated, "Счётчик 'Выполнено за всё время' не увеличился!"  

        with allure.step('Снова переходим в ленту заказов и проверяем значение счётчика'):
            main_page.click_order_feed()
                       
            final_total = order_feed_page.get_total_orders_count()
            allure.attach(f"Конечное значение: {final_total}", name="final_total",
                         attachment_type=allure.attachment_type.TEXT)
            
            assert final_total > initial_total, \
                f"Счётчик должен увеличиться. Было: {initial_total}, стало: {final_total}"


        
    @allure.title('При создании нового заказа счётчик "Выполнено за сегодня" увеличивается')
    def test_today_orders_counter_increases(self, login_authorized_profile):
        driver = login_authorized_profile
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)
        
        with allure.step('Переходим в ленту заказов и получаем начальное значение счётчика'):
            main_page.click_order_feed()
            initial_today = order_feed_page.get_today_orders_count()
            allure.attach(f"Начальное значение за сегодня: {initial_today}", name="initial_today",
                         attachment_type=allure.attachment_type.TEXT)
        
        with allure.step('Создаём заказ через API и получаем номер заказа'):
            access_token = main_page.get_access_token()
            order_number = order_feed_page.get_order_number_via_api_with_auth(access_token)
            allure.attach(f"Номер заказа: {order_number}", name="order_number",
                        attachment_type=allure.attachment_type.TEXT)
            
        with allure.step('Обновляем страницу для обновления данных'):
            driver.refresh()
            time.sleep(2)
        
        with allure.step('Ожидаем обновления счётчика "Выполнено за сегодня" в ленте заказов'):
            counter_updated = order_feed_page.wait_for_today_counter_update(initial_today)
            assert counter_updated, "Счётчик 'Выполнено за сегодня' не увеличился!"

        with allure.step('Снова переходим в ленту заказов и проверяем значение счётчика'):
            main_page.click_order_feed()
                       
            final_today = order_feed_page.get_today_orders_count()
            allure.attach(f"Конечное значение за сегодня: {final_today}", name="final_today",
                         attachment_type=allure.attachment_type.TEXT)
            
            assert final_today > initial_today, \
                f"Счётчик должен увеличиться. Было: {initial_today}, стало: {final_today}"

    
    
    @allure.title('После оформления заказа его номер появляется в разделе "В работе"')
    def test_order_number_appears_in_work_section(self, login_authorized_profile):
        driver = login_authorized_profile
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)
        
        with allure.step('Создаём заказ через API и получаем номер заказа'):
            access_token = main_page.get_access_token()
            order_number = order_feed_page.get_order_number_via_api_with_auth(access_token)
            allure.attach(f"Номер созданного заказа: {order_number}", name="order_number",
                         attachment_type=allure.attachment_type.TEXT)
        
        with allure.step('Переходим в ленту заказов'):
            main_page.click_order_feed()
        
        with allure.step('Ожидаем появления номера заказа в разделе "В работе"'):
            order_appeared = order_feed_page.wait_for_order_in_work(str(order_number))
            assert order_appeared, f"Номер заказа {order_number} не появился в разделе 'В работе'!"
        
        with allure.step('Проверяем, что номер заказа отображается в разделе "В работе"'):
            orders_in_work = order_feed_page.get_all_orders_in_work()
            allure.attach(f"Заказы в работе: {', '.join(orders_in_work)}", name="orders_in_work",
                        attachment_type=allure.attachment_type.TEXT)
            
            # Очищаем номера от ведущих нулей для сравнения
            orders_clean = [order.lstrip('0') for order in orders_in_work]
            
            assert str(order_number) in orders_clean, \
                f"Заказ {order_number} не найден в списке: {orders_in_work}"
            
