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

#     driver.get('https://shop.adidas.jp/products/IR8010/')
#     def parse(self, response):
#         driver.maximize_window()
#         img_src_list = None
#         try:
#             driver.maximize_window()
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.2)")
#             button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'showMoreButton')))
#             button.click()
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.4)")
#             driver.implicitly_wait(5)
#             article_image_wrapper = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.CLASS_NAME, 'article_image_wrapper.isExpand'))
#             )
#             img_elements = article_image_wrapper.find_elements(By.CLASS_NAME, 'test-img')

#             img_src_list = [img.get_attribute('src') for img in img_elements]
#         except Exception as e:
#             img_src_list = None
#             print('Exception occured', e)

#         #co-ordinated product
#         ##name, price, productnumber, imageurl, product page url
#         try:
#             driver.implicitly_wait(5)
#             footer_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.footerstickyClosebutton')))
#             footer_button.click()
#         except Exception as e: 
#             print("No footer button present" , e)

#         co_ordinate_products = []
#         try:
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.5)")
#             co_ordinate = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.CLASS_NAME, 'coordinate_box'))
#             )
#             li_elements = co_ordinate.find_elements(By.CSS_SELECTOR, 'li.carouselListitem')
#             for li in li_elements:
#                 li.click()
#                 time.sleep(5)
#                 coordinate_item_container = WebDriverWait(driver, 10).until(
#                     EC.presence_of_element_located((By.CSS_SELECTOR, 'div.coordinate_item_container.test-coordinate_item_container.add-open'))
#                 )
#                 product_link_element = coordinate_item_container.find_element(By.CLASS_NAME, 'image_wrapper')
#                 product_link = product_link_element.find_element(By.CLASS_NAME, 'test-link_a').get_attribute('href')
#                 product_number = product_link.split("/")
#                 co_ordinate_product_number = product_number[-1]
#                 product_image_element = coordinate_item_container.find_element(By.CLASS_NAME, 'image_wrapper')
#                 product_image = product_image_element.find_element(By.TAG_NAME, 'img').get_attribute('src')

#                 product_info_class = coordinate_item_container.find_element(By.CLASS_NAME, 'info_wrapper')
#                 product_title = product_info_class.find_element(By.CSS_SELECTOR, 'span.titleWrapper span.title').text
#                 product_price = product_info_class.find_element(By.CSS_SELECTOR, 'span.price-value').text

#                 product = {
#                     "product name": product_title,
#                     "product price": product_price,
#                     "product number": co_ordinate_product_number,
#                     "product image": product_image,
#                     "product url": product_link,
#                 }
#                 co_ordinate_products.append(product)
#                 time.sleep(5)

#         except Exception as e:
#             print("Exception occured: ", e)

#         yield {
#             'images': img_src_list,
#             'co-ordinate-products': co_ordinate_products
#         }
        
#     # driver.quit()

