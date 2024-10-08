from bs4 import BeautifulSoup
import re

class TecMundo:

    def __init__(self, html):
        self.html = html
        self.title = self.get_title()
        self.text = self.get_text()
        self.imageUrl, self.imageText = self.get_image()    


    def get_title(self):
        try:
            title = self.html.find('h1').get_text()
            return title.strip()
        except:
            return None


    def get_text(self):
        try:
            content = ""            
            contentBody = self.html.find('div', class_='tec--article__body').find_all('p')
            for p in contentBody:
                content += p.get_text()
                content += "\n"
            content = re.sub(r'\s+', ' ', content).strip()
            return content
        except:
            return None


    def get_image(self):
        try:
            image = self.html.find('figure', class_='tec--article__image__container')
            print(image)
            imageUrl = image.find('img').get('data-src')
            imageText = image.find('div').get_text()
            return imageUrl, imageText
        except:
            return None, None
