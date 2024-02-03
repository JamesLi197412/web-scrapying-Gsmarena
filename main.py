import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import urllib3
import time
import itertools
from crawler import Crawler
import json
from tokenBucket import TokenBucket

# Learning material: https://beautiful-soup-4.readthedocs.io/en/latest/#encodings

def web_browser(url,customHeaders,brandOption):
    crawler = Crawler()
    brands = crawler.brandNamePage(url,customHeaders)

    prodsDict = dict()

    for index, (brand,brandURL) in enumerate(brands.items()):
        if (brand.lower == brandOption):
            pass
        else:
            print('Currently working on Brand :' + brand + ' now')
            currPageNum, maxPageNum, links, brandSoup = crawler.brandProductsPageIntel(brandURL,customHeaders)

            brandDicts, _ = crawler.pageProduct(brandSoup, brand)
            prodSpecifications = []
            for prod in brandDicts:
                prodURL = url + '/' +brandDicts[prod]
                productDicts = crawler.productSpecs(prodURL, brand, prod, customHeaders)
                prodSpecifications.append(productDicts)

            prodsDict[brand] = prodSpecifications

    return prodsDict


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # main Page
    url = 'https://www.gsmarena.com'
    print('Start Crawing the website now')
    customHeaders ={
        "accept-language": "en-GB, en;q=0.9",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    }

    scral = Crawler()
    brandlist = scral.brandNamePage(url,customHeaders)
    for index, (brand, brandURL) in enumerate(brandlist.items()):
        print(index, brand)

    brand = input('Which phone brand you would love to view, here is a list of option\n 1 for apple, 2 for samsung etc')
    prodsDict = web_browser(url,customHeaders,brand)

    # export outcome to txt file
    with open('convert.txt', 'w') as convert_file:
        convert_file.write(json.dumps(prodsDict))

    print('Output file has been created yet. Job is done.')


