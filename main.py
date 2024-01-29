import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import urllib3
import time
import itertools
from crawler import Crawler
from tokenBucket import TokenBucket

# Learning material: https://beautiful-soup-4.readthedocs.io/en/latest/#encodings

def web_browser(url):
    crawler = Crawler()
    print('Start Crawing the website now')
    brands = crawler.brandNamePage(url)

    for index, (brand,brandURL) in enumerate(brands.items()):
        print('Crawing Information Brand by Brand now')
        print('Currently working on Brand :' + brand + 'now')

        #
        currPageNum, maxPageNum, links = crawler.brandProductsPageIntel(brandURL)

        # Current Page work
        brandSoup = crawler.getPage(brandURL)
        brandLists, brandCurrProd = crawler.pageProduct(brandSoup)

        print(brandCurrProd.head(10))




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # main Page
    url = 'https://www.gsmarena.com'

    web_browser(url)


