import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import urllib3
import time
import itertools
from crawler import Crawler
from tokenBucket import TokenBucket

def web_browser(url):
    crawler = Crawler()
    crawler.getPage(url)

    class_name = "bradmenu_v2 light 1-box clearfix"
    brands = crawler.brandNamePage(class_name, url)
    print(brands)

def web_test(url):
    # Example usage
    tokens_per_second = 2  # Adjust as needed
    bucket = TokenBucket(tokens_per_second)

    while True:
        if bucket.get_token():
            # Perform your web scraping operations here
            print("Scraping...")
            req = requests.get(url)
            soup = BeautifulSoup(req.text, 'html.parser')

        # Add some delay between subsequent requests
        time.sleep(1)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    url = 'https://www.gsmarena.com'
    web_test(url)
    #web_browser(url)


