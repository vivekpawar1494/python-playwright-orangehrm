import base64
import os
from datetime import datetime
import pytest
from playwright.sync_api import sync_playwright
from config.config import HEADLESS, BROWSER


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        if BROWSER == "chromium":
            browser = p.chromium.launch(
                headless=HEADLESS,
                args=["--start-maximized"]
            )
        elif BROWSER == "firefox":
            browser = p.firefox.launch(headless=HEADLESS)
        else:
            browser = p.webkit.launch(headless=HEADLESS)

        yield browser
        browser.close()

@pytest.fixture(scope="session")
def context(browser):
    from config.config import HEADLESS
    if HEADLESS:
        # Explicit viewport required in headless — no OS window available
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
    else:
        context = browser.new_context(no_viewport=True)
    yield context
    context.close()


@pytest.fixture(scope="session")
def context(browser):
    context = browser.new_context(no_viewport=True)
    yield context
    context.close()


@pytest.fixture(scope="session")
def page(context):
    page = context.new_page()
    yield page


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        page = item.funcargs.get("page", None)

        if page and not page.is_closed():
            project_root = os.path.dirname(os.path.abspath(__file__))
            screenshot_dir = os.path.join(project_root, "reports", "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)

            test_name = item.name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            status = "PASS" if report.passed else "FAIL"

            file_name = f"{test_name}_{status}_{timestamp}.png"
            path = os.path.join(screenshot_dir, file_name)

            # Wait for page to fully render before capturing
            page.wait_for_load_state("networkidle")
            page.screenshot(path=path, full_page=True)

            if item.config.pluginmanager.hasplugin("html"):
                import pytest_html
                extra = getattr(report, "extras", [])

                with open(path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode()

                extra.append(pytest_html.extras.image(encoded_string, mime_type="image/png"))
                report.extras = extra