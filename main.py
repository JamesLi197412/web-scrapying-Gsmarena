import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

import itertools
from crawler import Crawler

def web_browser(url):
    crawler = Crawler()
    crawler.getPage(url)
    print(crawler)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    url = 'https://www.gsmarena.com'
    web_browser(url)


