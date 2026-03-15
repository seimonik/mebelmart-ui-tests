import pytest
from playwright.sync_api import Page, expect

@pytest.mark.parametrize("sofa_name, expected_width", [("Диван Лидер", "2050")])
def test_sofa_details(page: Page, sofa_name: str, expected_width: str):
    """
    Проверка деталей товара в карточке дивана.
    Шаги:
    1. Открыть раздел "Диваны".
    2. Найти и кликнуть на диван "Диван Бостон".
    3. Проверить характеристики (ширина) в карточке товара.
    4. Убедиться, что значение совпадает с ожидаемым.
    """
    # Открыть страницу диванов
    page.goto("https://mebelmart-saratov.ru/myagkaya_mebel_v_saratove/divanyi_v_saratove")

    # Найти и кликнуть на диван по названию (текстовый локатор)
    sofa_item = page.locator(f"text={sofa_name}").first
    sofa_item.click()

    # Ожидание открытия новой страницы (явное ожидание URL)
    page.wait_for_url("**/id21cf4fa_divan_lider_meshkovina_rastsvetka_na_vyibor", timeout=5000)

    # Открыть характеристики дивана
    page.click("text=Характеристики")

    # Проверить наличие характеристики "Ширина" в карточке товара
    width_row = page.locator("tr:has-text('Ширина, мм.')")
    actual_width = width_row.locator("td:nth-child(2)").text_content().strip()

    assert expected_width in actual_width, (
        f"Ошибка: ожидаемая ширина {expected_width}, "
        f"фактическая: {actual_width}"
    )
