from functools import wraps
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


# set up browser
# needs Chrome and chromedriver
def get_browser(headless=False, minimize_on_start=False, load_main_config=False, proxy=None):
    # enables selenium to execute while browser trapping.
    des = DesiredCapabilities.CHROME
    des["pageLoadStrategy"] = "none"

    chrome_options = Options()
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('log-level=3')
    chrome_options.add_argument('--ignore-certificate-errors')

    if headless:
        chrome_options.add_argument('--headless')
    if load_main_config:
        chrome_options.add_argument(r'--user-data-dir=C:\Users\diodes\AppData\Local\Google\Chrome\User Data')
        chrome_options.add_argument('--profile-directory=Default')
    if proxy is not None:
        chrome_options.add_argument('--proxy-server={0}'.format(proxy))
    browser = Chrome(options=chrome_options, desired_capabilities=des)
    if minimize_on_start:
        browser.minimize_window()
    return browser
