from playwright.sync_api import Page, expect

from pages.sofas_page import SofasPage


# def test_divany_filter(page: Page):
#     divany_page = DivanyPage(page)
#     divany_page.goto()
#     divany_page.set_price_filter("10000", "15000")
#     divany_page.verify_product_visible("Диван Лотос")  # Цена ~12k руб., visible после фильтра [page:0]

def test_slider_drag(page, logger):
    logger.info("Запуск теста фильтрации диванов")
    sofas_page = SofasPage(page, logger)
    sofas_page.goto()
    # page.goto('https://mebelmart-saratov.ru/myagkaya_mebel_v_saratove/divanyi_v_saratove')

    # Скролл вниз на 500 пикселей
    page.mouse.wheel(0, 500)

    # Открыть область для фильтрации по цене
    # page.locator('.filter__title_checkbox >> text=Цена').click()
    sofas_page.price_filter_open()

    # Находим левый ползунок цены
    # slider_handle = page.locator('//div[@role="slider" and @aria-valuemin="4315" and contains(@class, "min-slider-handle")]')
    box_start = sofas_page.left_slider.bounding_box()

    # Находим правый ползунок цены
    # right_slider_handle = page.locator('//div[@role="slider" and @aria-valuemin="4315" and contains(@class, "max-slider-handle")]')
    box_end = sofas_page.right_slider.bounding_box()

    start_x = box_end['x'] + box_end['width'] / 2
    start_y = box_end['y'] + box_end['height'] / 2
    page.mouse.move(start_x, start_y)
    # page.mouse.down()

    logger.info(f'start_x={start_x}, start_y={start_y}')

    page.mouse.move(box_start['x'] + 20, start_y, steps=5)
    page.mouse.up()

    # sofas_page.apply_filter()
    sofas_page.verify_product_visible('Диван Гобелен')

    # expect(page.locator(f'text=Диван tetst')).to_be_visible()
