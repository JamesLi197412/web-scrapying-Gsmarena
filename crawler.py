import requests
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

        brands_dict = dict()

        for element in info:
            # access to link and brand_name
            link = element.a.get('href')
            brand_name = element.text

            brands_dict[brand_name] = url + link



        return brands_dict

    def safeGet(self, pageObj, selector):
        """

        :param pageObj:
        :param selector:
        :return:
        """
        selectedElems = pageObj.select(selector)
        if selectedElems is not None and len(selectedElems) > 0:
            return '\n'.join([elem.get_text() for elem in selectedElems])

        return ''

    def parse(self, site, url):
        """

        :param site:
        :param url:
        :return:
        """
        bs = self.getPage(url)
        if bs is not None:
            title = self.safeGet(bs, site.titleTag)
            body = self.safeGet(bs, site.bodyTag)

            if title != '' and body != '':
                content = Content(url, title, body)
                content.print()
