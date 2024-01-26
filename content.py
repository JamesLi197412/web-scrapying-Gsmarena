
class Content:
    def __init__(self,url,title,body):
        self.url = url
        self.title = title
        self.body = body

    def print(self):
        print("URL: {}".format(self.url))
        print('Title:{}'.format(self.title))
        print("BODY:\n")

    
