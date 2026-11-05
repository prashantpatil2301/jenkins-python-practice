import logging
from pathlib import Path

import pytest
from selenium import webdriver
from generate_report import create_pdf

logger = logging.getLogger(__name__)

URL = "https://www.prashantqa.com/Practice/index.html"


def pytest_configure(config):
    Path("reports").mkdir(exist_ok=True)


@pytest.fixture
def driver(request):
    logger.info("TEST START: %s", request.node.name)
    logger.info("Opening Chrome")

    browser = webdriver.Chrome()

    try:
        browser.maximize_window()
        logger.info("Navigating to %s", URL)
        browser.get(URL)

        yield browser
    finally:
        logger.info("Closing Chrome")
        browser.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        logger.info(
            "TEST RESULT: %s | %s",
            item.name,
            report.outcome.upper(),
        )

    elif report.failed:
        logger.error(
            "%s FAILED: %s",
            report.when.upper(),
            item.name,
        )

    if report.failed:
        logger.error("%s", report.longreprtext)

def pytest_sessionfinish(session, exitstatus):
    # Flush buffered log messages before reading the log file.
    for handler in logging.getLogger().handlers:
        handler.flush()

    create_pdf()