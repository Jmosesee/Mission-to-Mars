import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
headers = {'User-Agent': user_agent}

def get_Mars_news(url):
    # response = requests.get(url, headers = headers)
    # s = str(response.url).split('news')
    # api_url = s[0] + 'api/v1/news_items' + s[1]
    response = requests.get(url, headers = headers).json()
    item = response.get('items')[0]
    news_title = item.get('title')
    news_p = item.get('description')
    return (news_title, news_p)

def instantiate_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1420,1080')
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    return driver

def get_featured_image(driver, url):
    # Gets the featured image (not of Mars)
    driver.get("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")
    link = driver.find_element_by_id('full_image')
    href = link.get_attribute('data-fancybox-href')
    featured_image_url = "https://www.jpl.nasa.gov" + href
    return featured_image_url

def get_Mars_weather(url):
    response = requests.get(url, headers = headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    tweets = soup.find_all('div', class_ = 'tweet')
    for tweet in tweets:
        t = tweet.find('p').text
        if "Sol " in t:
            mars_weather = t
            break
    return mars_weather

def get_Mars_facts(url):
    df = pd.read_html(url, attrs={'id': 'tablepress-mars'})[0].set_index([0])
    df.columns = ['value']
    return df.to_html()

def get_Hemispheres(driver, url):
    driver.get(url)
    hemisphere_image_urls = []
    visited = []
    while True:
        links = driver.find_elements_by_class_name('itemLink')
        if all (link.get_attribute('href') in visited for link in links):
            break
        for link in links:
            href = link.get_attribute('href')
            if href in visited:
                continue
            else:
                try:
                    link.click()
                    img_url = str(driver.find_element_by_link_text("Sample").get_attribute('href'))
                    title = str(driver.find_elements_by_class_name('title')[0].text).rpartition(' ')[0]
                    hemisphere_image_urls.append({"title": title, "img_url": img_url})
                    driver.back()
                    visited.append(href)
                    break
                except:
                    continue
    return hemisphere_image_urls

def scrape():
    driver = instantiate_driver()
    (news_title, news_p) = get_Mars_news("https://mars.nasa.gov/api/v1/news_items/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc")
    featured_image_url = get_featured_image(driver, "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")
    mars_weather = get_Mars_weather("https://twitter.com/marswxreport?lang=en")
    mars_facts = get_Mars_facts("http://space-facts.com/mars/")
    hemisphere_image_urls = get_Hemispheres(driver, "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")
    driver.quit()
    return {
        "News Title": news_title,
        "News Description": news_p,
        "Featured Space Image": featured_image_url,
        "Mars Weather": mars_weather,
        "Mars Facts": mars_facts,
        "Hemispheres": hemisphere_image_urls,
    }
