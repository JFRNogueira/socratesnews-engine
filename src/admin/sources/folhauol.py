from bs4 import BeautifulSoup
import re

class FolhaUol:

    def __init__(self, html):
        self.html = html
        self.title = self.get_title()
        self.text = self.get_text()
        self.imageUrl, self.imageText = self.get_image()
    

    def get_title(self):
        try:
            title = self.html.find('h1', class_='c-content-head__title').get_text()
            return title.strip()
        except:
            return None


    def get_text(self):
        try:
            content = ""            
            contentBody = self.html.find('div', class_='c-news__body').find_all('p')
            for p in contentBody:
                content += p.get_text()
                content += "\n"
            content = re.sub(r'\s+', ' ', content).strip()
            return content
        except:
            return None


    def get_image(self):
        try:
            imageUrl = self.html.find('img', class_='img-responsive').get('data-src')
            imageText = self.html.find('figcaption', class_='widget-image').find('span').get_text()
            return imageUrl, imageText
        except:
            return None, None
        