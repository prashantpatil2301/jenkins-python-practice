import logging
from pathlib import Path
import os

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

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

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")

    if os.getenv("RUN_IN_DOCKER") == "true":
        options.binary_location = "/usr/bin/chromium"

        # Our learning container runs as root.
        options.add_argument("--no-sandbox")

        service = Service("/usr/bin/chromedriver")
        logger.info("Opening headless Chromium inside Docker")
        browser = webdriver.Chrome(
            service=service,
            options=options,
        )
    else:
        logger.info("Opening headless Chrome locally")
        browser = webdriver.Chrome(options=options)

    try:
        logger.info("Navigating to %s", URL)
        browser.get(URL)
        yield browser
    finally:
        logger.info("Closing browser")
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