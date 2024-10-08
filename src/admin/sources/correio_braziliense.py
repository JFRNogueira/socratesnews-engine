from bs4 import BeautifulSoup
import re

class CorreioBraziliense:

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
            contentBody = self.html.find('div', class_='cb-content-materia').find_all('p')
            for p in contentBody:
                content += p.get_text()
                content += "\n"
            content = re.sub(r'\s+', ' ', content).strip()
            return content
        except:
            return None


    def get_image(self):
        try:
            imageUrl = self.html.find('img', class_='cb-article-destaque').get('src')
            imageText = self.html.find('img', class_='cb-article-destaque').get('alt')
            return imageUrl, imageText
        except:
            return None, None