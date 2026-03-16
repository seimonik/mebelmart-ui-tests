from playwright.async_api import Page
from pages.sofas_page import SofasPage


def test_add_to_cart_price_check(page: Page, logger):
    """2.5 Добавление товара в корзину и проверка стоимости"""
        
    sofas_page = SofasPage(page, logger)
    sofas_page.goto()
    
    product_name, catalog_price = sofas_page.add_first_product_to_cart()
    
    sofas_page.go_to_cart()
    sofas_page.verify_cart_content("Модульный набор для кухни Лотос (Бител)", catalog_price) # Fix product_name
