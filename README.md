# MebelMart UI Tests

[![Python](https://img.shields.io/badge/Python-3.11+-brightgreen.svg)] [![Playwright](https://img.shields.io/badge/Playwright-1.42-blue.svg)] [![Pytest](https://img.shields.io/badge/Pytest-8.0-orange.svg)]

**Автотесты интернет-магазина МебельМарт** (Playwright + pytest + Page Object Model)

## Быстрый старт

```bash
# Клонировать репозиторий
git clone https://github.com/seimonik/mebelmart-ui-tests.git
cd mebelmart-ui-tests

# Установить зависимости
pip install -r requirements.txt
playwright install

# Запустить тесты (параллельно 2 потока)
pytest -n 2 -v -s --alluredir=allure-results

# Открыть Allure отчет
allure serve allure-results/
```

## Тестируемый функционал
* Фильтрация по характеристикам
* Характеристики товара в карточке
* Добавление товара в избранное
* Поиск товара по названию
* Корзина: добавление, проверка цены/количества

## Технический стек
* Фреймворк: Playwright + pytest + pytest-xdist
* Отчеты: Allure Framework
* Архитектура: Page Object Model
* Параллельность: 2-4 потока
* Браузер: Chromium (headless/headful)
* Разрешение: 1920x1080

## Allure отчеты
После запуска создается папка allure-results/. Отчет содержит:
* Скриншоты при ошибках
* Логи каждого шага
* Время выполнения
* Покрытие тестами
