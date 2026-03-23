import allure
from playwright.async_api import Page
import pytest
from pages.cart_page import CartPage
from pages.sofa_details_page import SofaDetailsPage
from pages.sofas_page import SofasPage


@pytest.mark.parametrize(
    "product_name, expected_favorite_name",
    [
        ("Диван замша", "Диван-книжка искусственная замша"),
    ],
)
@allure.title("Добавление '{product_name}' в корзину")
def test_add_to_cart_price_check(
    page: Page, logger, product_name: str, expected_favorite_name: str
):
    """5. Добавление товара в корзину и проверка стоимости"""

    sofas_page = SofasPage(page, logger)
    sofa_details_page = SofaDetailsPage(page, logger)
    cart_page = CartPage(page, logger)
    sofas_page.goto()

    catalog_price = sofas_page.get_product_price(product_name)
    sofas_page.add_product_to_cart(product_name)
    sofa_details_page.click_add_to_cart(expected_favorite_name)
    # page.wait_for_timeout(2000)
    # sofas_page.go_to_cart()
    
    cart_item_price = cart_page.get_item_price(expected_favorite_name)
    assert cart_item_price == catalog_price, f"Цена товара в корзине не совпала!"

    # Проверяем итого
    total_price = cart_page.get_total_sum()
    assert total_price == catalog_price, "Итоговая сумма не совпадает с ценой товара"
