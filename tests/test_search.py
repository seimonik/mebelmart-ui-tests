import allure
from playwright.async_api import Page
import pytest
from pages.search_page import SearchPage
from pages.sofas_page import SofasPage


@pytest.mark.parametrize("search_query", ["Бостон", "Лотос", "замша"])
@allure.title("Тестирование поискового запроса '{search_query}'")
def test_product_search(page: Page, logger, search_query: str):
    """4. Поиск товара по названию"""
    logger.info(f"Тест поиска: '{search_query}'")

    sofas_page = SofasPage(page, logger)
    search_page = SearchPage(page, logger)
    sofas_page.goto()

    sofas_page.search_product(search_query)
    search_page.verify_first_search_result(search_query)
