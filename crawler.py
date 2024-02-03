import requests
import pandas as pd

from urllib.error import HTTPError
from urllib.error import URLError

from bs4 import BeautifulSoup


class Crawler:
    def getPage(self, url,customHeaders):
        proxy = '127.0.0.1:9180'
        proxies ={
            'http':"http://" + proxy,
            'https': "https://" + proxy,
        }
        try:
            req = requests.get(url, headers = customHeaders)
            if req.status_code == 200:
                soup = BeautifulSoup(req.text, 'html.parser')
            elif req.status_code == 429:
                print('Unfortunately, Pages have been visited too much. You are suggested to visit the website later')
            else:
                print(req.status_code)

        except HTTPError as e:
            print(e)
            return None
        except URLError as e:
            print('The server could not be found')
            return None

        return soup

    def brandNamePage(self, mainurl,customHeaders):
        """

        :param class_name: 'bradmenu_v2 light 1-box clearfix'
        :param url:Home page of https://www.gsmarena.com/
        :return: return a dict (brand: brands' website)
        """
        soup = self.getPage(mainurl,customHeaders)
        info = soup.find('div', class_ = 'brandmenu-v2 light l-box clearfix')
        info = info.find('ul').find_all('li')

        brands_dict = dict()
        for element in info:
            brand_name = element.text
            brands_dict[brand_name] = mainurl + '/'+element.a.get('href') # vendor URL

        return brands_dict

    def brandProductsPageIntel(self, brandUrl,customHeaders):
        """
            Sweep through brand web (brand URL) includes its pages and record
            all product name, and their product url as well

        :param brandUrl: Brand URL, such as https://www.gsmarena.com/xiaomi-phones-80.php
        :return: df: cols = brand, product name within its brand, and its href & product url
        """
        brandsSoup = self.getPage(brandUrl,customHeaders)

        # current Page right now
        pagesList = brandsSoup.find_all("div", {'class':"section-body"})
        for tags in pagesList:
            if tags.select('strong'):
                currPageNumber = tags.select('strong')[0].text

        # Find out # of pages with this brand
        pagesList = brandsSoup.find("div", {"class":"section-body"})
        links = []
        #page_link = dict()
        for tags in pagesList.find_all('a'):
            link = tags.get('href')
            #page_link['Page Number' + tags.text] = link
            links.append(link)
        maxPageNumber = tags.text

        return currPageNumber, maxPageNumber,links,brandsSoup


    def pageProduct(self,brandSoup,brandName):
        """
            Sweep through brand web (brand URL) and record
            all product name, and their product url as well
            :param brandSoup:  soup of the current brand page, e.g. https://www.gsmarena.com/xiaomi-phones-80.php
            :return:
                dataframe or dict contains brand; product name; its url links
        """
        cols = ['Vendor', 'Product Name', 'Product Name Links']
        productLists = dict()

        # DF to store information
        productDf = pd.DataFrame(columns= cols)

        for child in brandSoup.find('div', {'class':'makers'}).ul.find_all('li'):
            product = child.text
            productLists[product] = child.a.get('href')

            df = pd.DataFrame([[brandName, product, child.a.get('href')]], columns = cols)
            productDf = pd.concat([productDf,df], ignore_index= True)

        return productLists,productDf


    def productSpecs(self, productUrl,brand,product,customHeaders):
        """
        Extract information from product page and convert it into DF
        :param productUrl:URL of the product
                brand: Vendor Name
                product: product name
        :return: Dataframe contains product all specification
        """
        soupProduct = self.getPage(productUrl,customHeaders)
        productPage = soupProduct.find('div', {'class':'main main-review right l-box col'})

        cols = [brand,product]
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


