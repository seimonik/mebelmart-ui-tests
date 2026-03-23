import allure
import pytest
from pages.sofas_page import SofasPage


@pytest.mark.parametrize(
    "style_name, expected_sofa_name",
    [
        ("лофт (loft)", "Диван Наоми"),
        ("минимализм", "Диван Лондон"),
        ("прованс", "Диван Рафаэль"),
    ],
    ids=["Лофт", "Минимализм", "Прованс"],
)
@allure.title("Фильтрация по стилю: {style_name}")
def test_sofa_style_filter(page, logger, style_name: str, expected_sofa_name: str):
    """1. Фильтрация по характеристикам и проверка наличия товара"""
    allure.dynamic.description(
        f"Проверяет фильтр стиля {style_name} на странице диванов"
    )

    logger.info("Запуск теста фильтрации диванов по стилю")
    sofas_page = SofasPage(page, logger)
    sofas_page.goto()

    filter_name = "Стиль"

    sofas_page.filter_open(filter_name)
    sofas_page.choose(filter_name, style_name)
    sofas_page.apply_filter()

    sofas_page.verify_product_visible(expected_sofa_name)


@pytest.mark.parametrize(
    "style_name, expected_sofa_name",
    [
        ("да", "Диван Фарадей"),
        ("нет", "Диван Бильбао"),
    ],
    ids=["С подлокотниками", "Без подлокотников"],
)
@allure.title("Фильтрация по наличию подлокотников: {style_name}")
@allure.description("Проверяет фильтрацию по наличию подлокотников у дивана")
def test_sofa_armrests_filter(page, logger, style_name: str, expected_sofa_name: str):
    """1. Фильтрация по характеристикам и проверка наличия товара"""

    logger.info("Запуск теста фильтрации диванов по стилю")
    sofas_page = SofasPage(page, logger)
    sofas_page.goto()

    filter_name = "Подлокотники"

    sofas_page.filter_open(filter_name)
    sofas_page.choose(filter_name, style_name)
    sofas_page.apply_filter()

    sofas_page.verify_product_visible(expected_sofa_name)
