from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#import subprocess
import time
from selenium.webdriver.common.proxy import Proxy, ProxyType
def create_chrome_driver():

    # chrome_path = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    # subprocess.Popen([chrome_path, '--remote-debugging-port=9222'])
    # time.sleep(3)
    # prox = Proxy()
    # prox.proxy_type = ProxyType.MANUAL
    # prox.autodetect = False
    # prox.http_proxy = "127.0.0.1:9150"
    # prox.ssl_proxy = "127.0.0.1:9150"
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    options.add_argument("--start-maximized")

    # options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    # options.add_argument('--proxy-server=socks5://127.0.0.1:9150')
    # options.add_argument('--disable-web-security')

    driver = webdriver.Chrome(options=options)
    return driver

def create_category_url(category):
    base_url = "https://www.udemy.com/courses/development/"
    return base_url + category

def find_num_pages(categories):
    driver = create_chrome_driver()
    pages_by_category = []
    for category in categories:
        print(category, end = ' ')
        url = create_category_url(category)
        driver.get(url)
        driver.implicitly_wait(10)
        wait = WebDriverWait(driver, 10)
        try:
            element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'span.ud-heading-sm.pagination-module--page--1Ujec')))
            text = element.text
            print(text)
            pages_by_category.append(int(text))
        except TimeoutException:
            print("Timed out while waiting for page number")
            pages_by_category.append(0)
    driver.quit()
    return pages_by_category

def get_lecture_details(categories, pages_by_category):
    driver = create_chrome_driver()
    for idx, category in enumerate(categories):
        last_page = pages_by_category[idx]
        for pg in range(1,last_page+1):
            url = create_category_url(category) + "?p=" +pg
            pass


if __name__ == "__main__":
    categories = ["web-development/","data-science/","mobile-apps/","programming-languages/","game-development/","databases/","software-testing/","software-engineering/","development-tools/","no-code-development/"]
    pages_by_category = find_num_pages(categories)
    get_lecture_details(categories, pages_by_category)