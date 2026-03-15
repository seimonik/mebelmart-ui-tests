import re
from playwright.async_api import Page
from playwright.sync_api import sync_playwright, expect
import pytest
from pages.sofas_page import SofasPage


@pytest.mark.parametrize(
    "product_name, expected_favorite_name",
    [
        ("Диван Лотос", "Модульный набор для кухни Лотос"),
        ("Диван Мешковина", "Еврокнижка выкатная мешковина Волод"),
        ("Диван замша", "Диван-книжка искусственная замша"),
    ],
)
def test_favorites(page: Page, logger, product_name: str, expected_favorite_name: str):
    sofas_page = SofasPage(page, logger)
    sofas_page.goto()
    sofa_name = sofas_page.add_product_to_favorites_by_name(product_name)

    sofas_page.go_to_favorites()

    expect(sofas_page.page.locator(f"text={expected_favorite_name}")).to_be_visible()
    logger.info(f"'{expected_favorite_name}' найден в Избранном!")
