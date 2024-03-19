import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# cap = DesiredCapabilities().FIREFOX
# cap["marionette"] = False
# executeable_path = 'E:\\geckodriver.exe'
# driver = webdriver.Firefox(options=)

driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

class testSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['www.shop.adidas.jp/']
    start_urls = ['https://shop.adidas.jp/']

    driver.get('https://shop.adidas.jp/products/IS3833/')
    def parse(self, response):
        driver.maximize_window()
        page_height = driver.execute_script("return document.body.scrollHeight")
        scroll_increment = 80 
        scroll_delay = 0.1      
        scroll_position = 0
        while scroll_position < page_height:
            driver.execute_script(f"window.scrollTo(0, {scroll_position});")
            time.sleep(scroll_delay)
            scroll_position += scroll_increment

        special_function = None
        try:
            special_category_name = driver.find_element(By.CSS_SELECTOR, '.item_part.details a').text
            special_category_description = driver.find_element(By.CSS_SELECTOR, '.item_part.details').text
            special_function = special_category_name + ': ' + special_category_description
        except Exception as e:
            special_function = "No special function"
            print("Exception occured: ", e)

        yield {
            'special function': special_function
        }
        
    # driver.quit()

