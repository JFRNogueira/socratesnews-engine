from bs4 import BeautifulSoup
import re

class CnnBrasil:

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
            contentBody = self.html.find('div', class_='single-content').find_all('p')
            for p in contentBody:
                content += p.get_text()
                content += "\n"
            content = re.sub(r'\s+', ' ', content).strip()
            return content
        except:
            return None


    def get_image(self):
        try:
            image = self.html.find('figure', class_="featured-image")
            imageUrl = image.find('img').get('src')
            imageText = image.find('figcaption').find('span', class_='featured-image__credit').get_text()
            return imageUrl, imageText
        except:
            return None, None