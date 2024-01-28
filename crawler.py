import requests
import pandas as pd
from bs4 import BeautifulSoup
from content import Content

class Crawler:
    def getPage(self, url):
        try:
            req = requests.get(url)

            if req.status_code == 200:
                soup = BeautifulSoup(req.text, 'html.parser')
            else:
                print(req.status_code)

        except requests.exceptions.RequestException:
            return None

        return soup

    def brandNamePage(self, class_name, url):
        soup = self.getPage(url)
        parent = soup.find("div", class_ = class_name)
        info = parent.ul.find_all('li')

        # Generate empty dict to store brands and its next page
        brands_dict = dict()

        for element in info:
            # access to link and brand_name
            link = element.a.get('href')
            brand_name = element.text

            brands_dict[brand_name] = url + link



        return brands_dict

    def brandProducts(self,class_name,url):
        brand_dict = self.brandNamePage(url,class_name)
        for index, value in brand_dict:
            #
            soup_brand = self.getPage(value)


            print(value)

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


    def safeGet(self, pageObj, selector):
        selectedElems = pageObj.select(selector)
        if selectedElems is not None and len(selectedElems) > 0:
            return '\n'.join([elem.get_text() for elem in selectedElems])

        return ''

    def parse(self, site, url):
        bs = self.getPage(url)
        if bs is not None:
            title = self.safeGet(bs, site.titleTag)
            body = self.safeGet(bs, site.bodyTag)

            if title != '' and body != '':
                content = Content(url, title, body)
                content.print()
