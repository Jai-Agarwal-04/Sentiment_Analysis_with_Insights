

import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
import sqlite3 as sql
from webdriver_manager.chrome import ChromeDriverManager
urls = []
product_urls = []
list_of_reviews = []


def initialize_urls():
    # Each page urls
    for i in range(4, 200):
        urls.append(
            f"https://www.etsy.com/in-en/c/jewelry-and-accessories?ref=pagination&page={i}")


def scrapping_urls():
    # Scrapping each product's urls | 16,064 products
    for url in urls:
        try:
            
                    
        
            driver = webdriver.Chrome(ChromeDriverManager().install())
            driver.get(url)
            sleep(2)
            for i in range(1, 65):
                product = driver.find_element_by_xpath(
                        f'/html/body/div[5]/div/div[1]/div/div[3]/div[2]/div[2]/div[6]/div/div/div/ul/li{[i]}/div/a')
                product_urls.append(product.get_attribute('href'))
                
        except:
            continue
        
    driver.close()

                    
        




def scrap_data():
    # Scrapping each product's reviews
    driver = webdriver.Chrome(ChromeDriverManager().install())
    for product_url in product_urls:
        try:
            driver.get(product_url)
            sleep(2)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html')

            text = soup.find(
                'button', {'id': 'same-listing-reviews-tab'}).getText().split()[:-1]

            text = ' '.join(text)

            if text:
                for i in range(4):
                    try:
                        list_of_reviews.append(soup.select(
                            f'#review-preview-toggle-{i}')[0].getText().strip())
                    except:
                        continue
                while(True):
                    try:
                        next_button = driver.find_element_by_xpath(
                            '//*[@id="reviews"]/div[2]/nav/ul/li[position() = last()]/a[contains(@href, "https")]')
                        if next_button != None:
                            next_button.click()
                            sleep(3)
                            html = driver.page_source
                            soup = BeautifulSoup(html, 'html')
                            for i in range(4):
                                try:
                                    list_of_reviews.append(soup.select(
                                        f'#review-preview-toggle-{i}')[0].getText().strip())
                                except:
                                    continue
                    except Exception as e:
                        break
        except:
            continue
    driver.close()


if __name__ == '__main__':
    initialize_urls()
    scrapping_urls()
    scrap_data()

    scrappedReviews = pd.DataFrame(
    list_of_reviews, index=None, columns=['reviews'])
    scrappedReviews.to_csv('etsy_swimwear_reviews.csv')

    df = pd.read_csv('etsy_reviews.csv')
    conn = sql.connect('etsy_reviews.db')
    df.to_sql('reviews', conn)
