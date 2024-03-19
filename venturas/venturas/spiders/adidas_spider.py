import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))


class AdidasSpider(scrapy.Spider):
    name = 'adidas'
    allowed_domains = ['www.shop.adidas.jp/']
    start_urls = ['https://shop.adidas.jp/']

    # driver.get('https://shop.adidas.jp/products/IR8010/')
    driver.get('https://shop.adidas.jp/item/?gender=mens&category=wear&order=1&limit=120&page=1')

    def parse(self, response):
        driver.maximize_window()
        all_cards = []
        page_height = driver.execute_script("return document.body.scrollHeight")
        scroll_increment = 80 
        scroll_delay = 0.1      
        scroll_position = 0
        while scroll_position < page_height:
            driver.execute_script(f"window.scrollTo(0, {scroll_position});")
            time.sleep(scroll_delay)
            scroll_position += scroll_increment

        item_cards = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'itemCardArea-cards.test-card.css-dhpxhu')))
        for card in item_cards:
            card_url = card.find_element(By.CSS_SELECTOR, 'a.image_link').get_attribute('href')
            all_cards.append(card_url)
           
        driver.implicitly_wait(2)
        # for individual testing
        # all_cards = ['https://shop.adidas.jp/products/IR8010/', 'https://shop.adidas.jp/products/IN6234/']
        for card in all_cards:
            try:
                driver.get(card)
                print("Start Scraping from: ", card)
                #current url
                current_product_link = driver.current_url

                #breadcrumb
                breadcrumb_elements = driver.find_elements(By.CLASS_NAME, 'breadcrumbListItem')
                breadcrumbs = [item.text for item in breadcrumb_elements]

                # category
                category_name_class = driver.find_element(By.CLASS_NAME, 'groupName')
                category_names = category_name_class.find_elements(By.TAG_NAME, 'span')
                category = ' '.join(name.text for name in category_names)

                #product name
                product_name = driver.find_element(By.CLASS_NAME, 'itemTitle').text

                #price
                price = driver.find_element(By.CSS_SELECTOR, '.articlePrice span').text

                #available sizes
                
                available_sizes = []
                try:
                    all_sizes = driver.find_elements(By.CSS_SELECTOR, '.sizeSelectorListItemButton:not(.disable)')
                    for size in all_sizes:
                        available_sizes.append(size.text)
                except:
                    available_sizes = "No available sizes"

                # sense of the size
                sense_text = None
                try:
                    sense = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div._root_07f8c._reset_a112d._sizeTextWrapper_cf9bf'))
                    )
                    sense_text = sense.find_element(By.CSS_SELECTOR, 'span._root_7a104._reset_a112d._blockLevel_7a104._normal_7a104._bold_7a104._whiteSpacePreLine_7a104').text

                except Exception as e:
                    sense_text = None
                    print("Exception occured: ", e)

                #product images
                img_src_list = None
                try:
                    driver.maximize_window()
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.2)")
                    button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'showMoreButton')))
                    button.click()
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.4)")
                    driver.implicitly_wait(5)
                    article_image_wrapper = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'article_image_wrapper.isExpand'))
                    )
                    img_elements = article_image_wrapper.find_elements(By.CLASS_NAME, 'test-img')

                    img_src_list = [img.get_attribute('src') for img in img_elements]
                except Exception as e:
                    img_src_list = None
                    print('Exception occured', e)

                #close pop-up
                try:
                    driver.implicitly_wait(5)
                    footer_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.footerstickyClosebutton')))
                    footer_button.click()
                except Exception as e: 
                    print("No footer button present" , e)

                #co-ordinated product
                ##name, price, productnumber, imageurl, product page url
                co_ordinate_products = []
                try:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.5)")
                    co_ordinate = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'coordinate_box'))
                    )
                    li_elements = co_ordinate.find_elements(By.CSS_SELECTOR, 'li.carouselListitem')
                    for li in li_elements:
                        li.click()
                        time.sleep(5)
                        coordinate_item_container = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.coordinate_item_container.test-coordinate_item_container.add-open'))
                        )
                        product_link_element = coordinate_item_container.find_element(By.CLASS_NAME, 'image_wrapper')
                        product_link = product_link_element.find_element(By.CLASS_NAME, 'test-link_a').get_attribute('href')
                        product_number = product_link.split("/")
                        co_ordinate_product_number = product_number[-1]
                        product_image_element = coordinate_item_container.find_element(By.CLASS_NAME, 'image_wrapper')
                        product_image = product_image_element.find_element(By.TAG_NAME, 'img').get_attribute('src')

                        product_info_class = coordinate_item_container.find_element(By.CLASS_NAME, 'info_wrapper')
                        product_title = product_info_class.find_element(By.CSS_SELECTOR, 'span.titleWrapper span.title').text
                        product_price = product_info_class.find_element(By.CSS_SELECTOR, 'span.price-value').text

                        product = {
                            "product name": product_title,
                            "product price": product_price,
                            "product number": co_ordinate_product_number,
                            "product image": product_image,
                            "product url": product_link,
                        }
                        co_ordinate_products.append(product)
                        time.sleep(5)

                except Exception as e:
                    print("Exception occured: ", e)
                
                page_height = driver.execute_script("return document.body.scrollHeight")
                scroll_increment = 60 
                scroll_delay = 0.1      
                scroll_position = 0
                while scroll_position < page_height:
                    driver.execute_script(f"window.scrollTo(0, {scroll_position});")
                    time.sleep(scroll_delay)
                    scroll_position += scroll_increment

                #title of the description
                try:
                    description_title = driver.find_element(By.CSS_SELECTOR, '.inner h2').text
                except:
                    description_title = None

                #general description of the product
                try:
                    general_description = driver.find_element(By.CSS_SELECTOR, '.commentItem-mainText').text
                except:
                    general_description = None
                #general description (itemization)
                #response.css('.articleFeatures li::text').getall()

                try:
                    description_points = driver.find_elements(By.CSS_SELECTOR, '.articleFeatures li')
                    general_description_itemized = [item.text for item in description_points]
                except:
                    general_description_itemized = None
                #special function if any
                special_function = None
                try:
                    special_category_name = driver.find_element(By.CSS_SELECTOR, '.item_part .details a').text
                    special_category_description = driver.find_element(By.CSS_SELECTOR, '.item_part.details').text
                    special_function = special_category_name + ': ' + special_category_description
                except Exception as e:
                    special_function = "No special function"
                    print("Exception occured: ", e)
                
                #product size chart
                try:
                    sizeChart = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.sizeChart')))
                    row_main_name = sizeChart.find_element(By.CLASS_NAME, 'sizeChartTHeader')
                    header_cells = row_main_name.find_elements(By.TAG_NAME, 'th')
                    row_names = [cell.text.strip() for cell in header_cells]

                    row_details = []
                    cells = sizeChart.find_elements(By.CSS_SELECTOR, 'tr.sizeChartTRow')
                    for cell in cells:
                        row_detail = cell.find_elements(By.CSS_SELECTOR, 'td.sizeChartTCell')
                        all_row_values = []
                        for item in row_detail:
                            tag = item.find_element(By.TAG_NAME, 'span').text.strip()
                            all_row_values.append(tag)
                        
                        row_details.append(all_row_values)           
                except:
                    row_names = None
                    row_details = None

                #rating, number of reviews, recommended rate
                try:
                    all_rating_info = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'BVRRQuickTakeCustomWrapper')))
                    rating_class = all_rating_info.find_element(By.CLASS_NAME, 'BVRRRatingNormalOutOf')
                    rating = rating_class.find_element(By.TAG_NAME, 'span').text

                    rating_count_class = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'BVRRNumber.BVRRBuyAgainTotal')))
                    review_count = rating_count_class.text

                    rating_percentage_class = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'BVRRBuyAgainPercentage')))
                    rating_percentage = rating_percentage_class.text
                except:
                    rating = None
                    review_count = None
                    rating_percentage = None

                #user review information: date, rating, review title, review description, reviewer ID
                all_reviews = []
                try:
                    all_review_classes = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'BVRRContentReview')))
                    for review_class in all_review_classes:
                        star = review_class.find_element(By.CLASS_NAME, 'BVImgOrSprite').get_attribute('title')
                        title = review_class.find_element(By.CSS_SELECTOR, 'span.BVRRValue.BVRRReviewTitle').text
                        review_text = review_class.find_element(By.CSS_SELECTOR, 'span.BVRRReviewText').text
                        user = review_class.find_element(By.CSS_SELECTOR, 'span.BVRRNickname').text
                        date = review_class.find_element(By.CSS_SELECTOR, 'span.BVRRValue.BVRRReviewDate').text

                        review = {
                            'user': user,
                            'date of review': date,
                            'star': star,
                            'review title': title,
                            'review text': review_text
                        }

                        all_reviews.append(review)
                except:
                    all_reviews = None

                #review rating of each item, such as, sense of fitting + its rating, appr ... comfort
                all_fit_sense = None
                try:
                    driver.implicitly_wait(10)
                    all_fit_sense = []
                    fit_sense_classes = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'BVRRCustomRatingEntryWrapper')))
                    for fit_sense_class in fit_sense_classes:
                        label_classes = fit_sense_class.find_elements(By.CLASS_NAME, 'BVRRRatingEntry')
                        for label_class in label_classes:
                            label = label_class.find_element(By.CLASS_NAME, 'BVRRRatingHeader').text
                            value = label_class.find_element(By.CLASS_NAME, 'BVImgOrSprite').get_attribute('title') 
                            fit_sense = {
                                'label': label,
                                'value': value
                            }
                            all_fit_sense.append(fit_sense)
                except Exception as e:
                    print("Exception", e)
                
                #Keywords below
                tags = []
                try:
                    item_tags = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'itemTagsPosition')))
                    all_tags = item_tags.find_elements(By.TAG_NAME, 'a')
                    for tag in all_tags:
                        tags.append(tag.text)
                        
                except Exception as e:
                    tags = None
                    print("Exception", e)

                data = {
                    'Product URL': current_product_link,
                    'Breadcrumbs': breadcrumbs,
                    'Product Category': category,
                    'Product Name': product_name,
                    'Product Price(¥)': price,
                    'Available Sizes': available_sizes,
                    'Sense of size': sense_text,
                    'Product Images': img_src_list,
                    'Co-ordinated Products': co_ordinate_products,
                    'Description Title': description_title,
                    'General Description': general_description,
                    'General Description Itemized': general_description_itemized,
                    'Special Function': special_function,
                    'Product Size Chart': {
                        'Criteria': row_names,
                        'Values': row_details
                    },
                    'Overall Product Rating': rating,
                    'Overall Review Count': review_count,
                    'Overall Review Percentage': rating_percentage,
                    'All User Reviews': all_reviews,
                    'Overall Fit Sense': all_fit_sense,
                    'Keywords': tags
                }
                yield data

                # filename = 'product.txt'
                # with open(filename, 'a', encoding='utf-8') as file:
                #     file.write('\n')
                #     json.dump(data, file, indent=4, ensure_ascii=False)

                print("Finished scraping from: ", card)
            except Exception as e:
                print("Exception: ", e)
                continue
            
            