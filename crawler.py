import requests
import pandas as pd
import numpy as np

from urllib.error import HTTPError
from urllib.error import URLError
from urllib.request import urlopen

from bs4 import BeautifulSoup

from content import Content

class Crawler:
    def getPage(self, url):
        try:
            req = requests.get(url)
            if req.status_code == 200:
                soup = BeautifulSoup(req.text, 'html.parser')
            elif req.status_code == 429:
                print('Unfortunately, Pages have been visited too much. You are suggested to visit the website later')
            else:
                print(req.status_code)

        except HTTPError as e:
            print(e)
        except URLError as e:
            print('The server could not be found')
            return None

        return soup

    def brandNamePage(self, mainurl):
        """

        :param class_name: 'bradmenu_v2 light 1-box clearfix'
        :param url:Home page of https://www.gsmarena.com/
        :return: return a dict (brand: brands' website)
        """
        soup = self.getPage(mainurl)
        info = soup.find('div', {'class': 'bradmenu_v2 light 1-box clearfix'}).ul.find_all('li')

        # Generate empty dict to store brands and its next page
        brands_dict = dict()
        for element in info:
            # access to link and brand_name
            brand_name = element.text
            brands_dict[brand_name] = mainurl + element.a.get('href')

        return brands_dict

    def brandProducts(self,brandUrl):
        """
        Sweep through brand web (brand URL) includes its pages and record
        all product name, and their product url as well

        :param brandUrl: Brand URL, such as https://www.gsmarena.com/xiaomi-phones-80.php
        :return: df: cols = brand, product name within its brand, and its href & product url
        """
        #
        brandsSoup = self.getPage(brandUrl)

        # Find out # of pages with this brand
        pagesList = brandsSoup.find_all("div", {"class":"nav-pages"})
        page_link = dict()
        for tags in pagesList:
            if (tags.select('strong')):
                currPageNumber = tags.select('strong')[0].text
                print(currPageNumber)
            elif tags.select('a'):
                print(tags.select('a').text)


        # Find out all contents/products on current page
        # to get href & product_name
        # output will be another dict
        productLists = dict()
        for child in brandsSoup.find('div', {'class':'makers'}).ul.find_all('li'):
            product = child.text
            productLists[product] = child.a.get('href')



    def productSpecs(self, productUrl):
        """
        Extract information from product page and convert it into DF
        :param productUrl:URL of the product
        :return: Dataframe contains product all specification
        """
        soupProduct = self.getPage(productUrl)
        productPage = soupProduct.find('div', {'class':'main main-review right l-box col'})

        cols = []
        # Extract col Names from the site
        for title in productPage.find_all('td',{'class':'ttl'}):
            cols.append(title.text)

        prodDf = pd.DataFrame(columns = cols)

        # Feed intel into the dataframe
        intel = []
        for specs in productPage.find_all('td', {'class':'nfo'}):
            intel.append(specs.text)

        prodDf = prodDf.append(pd.DataFrame([intel], columns=cols), ignore_index= True)

        return prodDf


