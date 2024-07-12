
import time
from threading import Thread
import pyautogui
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

hostname = "161.77.171.5"
port = "50100"
proxy_username = "zabutniy20"
proxy_password = "XHt7nTwPHW"

chrome_options = Options()
chrome_options.add_argument('--proxy-server={}'.format(hostname + ":" + port))
driver = webdriver.Chrome(options=chrome_options)


def enter_proxy_auth(proxy_username, proxy_password):
    time.sleep(1)
    pyautogui.typewrite(proxy_username)
    pyautogui.press('tab')
    pyautogui.typewrite(proxy_password)
    pyautogui.press('enter')


def open_a_page(driver, url):
    driver.get(url)


Thread(target=open_a_page, args=(driver, "https://www.paginasamarillas.es/search/nutricionistas/all-ma/all-pr/all-is/all-ci/all-ba/all-pu/all-nc/1?what=Nutricionistas&qc=true")).start()
Thread(target=enter_proxy_auth, args=(proxy_username, proxy_password)).start()


time.sleep(60)