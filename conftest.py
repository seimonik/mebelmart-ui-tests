from datetime import datetime
import logging
import re
import pytest
import allure
from pathlib import Path
import os
import shutil
import tempfile
from playwright.sync_api import Page
from pages.sofas_page import SofasPage

SCREENSHOT_NAME_PATTERN = re.compile(r"^test-failed-\d+\.png$")


# Настройка логгера
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file = f"{log_dir}/test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(),  # В консоль
    ],
)


@pytest.fixture(scope="session")
def logger():
    """Глобальный logger для всех тестов"""
    return logging.getLogger(__name__)


# Автоприменяемая фикстура для output_dir (как в playwright-pytest)
@pytest.fixture(scope="session", autouse=True)
def output_path():
    output_dir = "test-results"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    yield output_dir


@pytest.fixture(scope="session")
def browser_context(browser, output_path):
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    yield context
    context.close()


@pytest.fixture(scope="session")
def browser_context_args():
    """Общие настройки для изоляции потоков"""
    return {
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
        "java_script_enabled": True,
    }


@pytest.fixture(scope="function")
def page(request, playwright, browser_context_args):
    """Новая страница для каждого теста (изоляция)"""
    browser = playwright.chromium.launch(headless=False)  # headed=True для отладки
    context = browser.new_context(**browser_context_args)
    page = context.new_page()

    yield page

    context.close()
    browser.close()


@pytest.fixture
def page(browser_context):
    page = browser_context.new_page()
    yield page
    page.close()


@pytest.fixture
def divany_page(page: Page):
    return SofasPage(page)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        page_obj = item.funcargs.get("page")
        if page_obj:
            page_obj.screenshot(path="test-results/test-failed.png", full_page=True)
            allure.attach(
                "test-results/test-failed.png",
                "failure_screenshot",
                attachment_type=allure.attachment_type.PNG,
            )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_teardown(item, nextitem):
    yield
    artifacts_dir = item.funcargs.get("output_path")
    if artifacts_dir and Path(artifacts_dir).is_dir():
        for file in Path(artifacts_dir).iterdir():
            if file.suffix == ".png":
                allure.attach.file(
                    str(file),
                    name=file.name,
                    attachment_type=allure.attachment_type.PNG,
                )
