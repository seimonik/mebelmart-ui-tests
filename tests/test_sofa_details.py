import pytest
from playwright.sync_api import Page
from pages.sofas_page import SofasPage
from pages.sofa_details_page import SofaDetailsPage


@pytest.mark.parametrize(
    "sofa_name, expected_width, sofa_id",
    [
        (
            "Диван Лидер",
            "2050",
            "id21cf4fa_divan_lider_meshkovina_rastsvetka_na_vyibor", # id из url'а
        ),
        (
            "Диван разные расцветки",
            "2200",
            "idbf109a6_evroknijka_vyikatnaya_iskusstvennaya_zamsha_v-d"
        )
    ],
)
def test_sofa_details(
    page: Page, logger, sofa_name: str, expected_width: str, sofa_id: str
):
    """
    Проверка деталей товара в карточке дивана.
    Шаги:
    1. Открыть раздел "Диваны".
    2. Найти и кликнуть на диван "Диван Бостон".
    3. Проверить характеристики (ширина) в карточке товара.
    4. Убедиться, что значение совпадает с ожидаемым.
    """

    sofas_page = SofasPage(page, logger)
    sofa_details_page = SofaDetailsPage(page, logger)

    sofas_page.goto()
    sofas_page.find_and_click_sofa(sofa_name)
    sofa_details_page.wait_for_page_load(sofa_id)
    sofa_details_page.open_characteristics()
    actual_width = sofa_details_page.get_sofa_width()

    assert expected_width in actual_width, (
        f"Ошибка: ожидаемая ширина {expected_width}, " f"фактическая: {actual_width}"
    )
