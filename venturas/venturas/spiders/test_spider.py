# import scrapy
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.firefox.service import Service
# # from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.firefox import GeckoDriverManager
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time

# # from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# # cap = DesiredCapabilities().FIREFOX
# # cap["marionette"] = False
# # executeable_path = 'E:\\geckodriver.exe'
# # driver = webdriver.Firefox(options=)

# driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

# class testSpider(scrapy.Spider):
#     name = 'test'
#     allowed_domains = ['www.shop.adidas.jp/']
#     start_urls = ['https://shop.adidas.jp/']

#     driver.get('https://shop.adidas.jp/products/IZ4922/')
#     def parse(self, response):
#         # page_height = driver.execute_script("return document.body.scrollHeight")
#         # scroll_increment = 80 
#         # scroll_delay = 0.1      
#         # scroll_position = 0
#         # while scroll_position < page_height:
#         #     driver.execute_script(f"window.scrollTo(0, {scroll_position});")
#         #     time.sleep(scroll_delay)
#         #     scroll_position += scroll_increment
#         # driver.maximize_window()
#         # driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.3)")
#         driver.implicitly_wait(3)
#         sense_text = None
#         try:
#             sense = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, 'div._root_07f8c._reset_a112d._sizeTextWrapper_cf9bf'))
#             )
#             sense_text = sense.find_element(By.CSS_SELECTOR, 'span._root_7a104._reset_a112d._blockLevel_7a104._normal_7a104._bold_7a104._whiteSpacePreLine_7a104').text

#         except Exception as e:
#             sense_text = None
#             print("Exception occured: ", e)

#         yield {
#             'sense': sense_text
#         }
        
#     # driver.quit()

