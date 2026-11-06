import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


logger = logging.getLogger(__name__)


def test_page_title(driver):
    expected_title = "My SDET Academy | Selenium Lab"

    logger.info("Checking page title")
    logger.info("Expected title: %s", expected_title)

    try:
        WebDriverWait(driver, 10).until(
            EC.title_is(expected_title)
        )
    finally:
        logger.info("Actual title: %s", driver.title)

    assert driver.title == expected_title


def test_login_email_present(driver):
    logger.info(
        "Checking for an input element with id='login-email'"
    )

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input#login-email")
        )
    )

    logger.info("Login email input found in the DOM")
    assert element is not None