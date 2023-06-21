#
# EPITECH PROJECT, 2023
# scrapping_wttj
# File description:
# setup_driver.py
#

from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os


def setup_driver(link, headless_mode):
    # setup all driver settings
    path = ChromeDriverManager().install()
    os.environ['PATH'] = 'Valeur de ma variable'
    print(path)
    print(os.environ['PATH'])
    s = Service(path)
    # print(os.path.abspath('./chromedriver'))
    # s = Service(os.path.abspath('./chromedriver'))
    chrome_options = Options()
    if headless_mode == "False":
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=s, options=chrome_options)
    driver.maximize_window()
    driver.get(link)
    sleep(5)
    return driver

