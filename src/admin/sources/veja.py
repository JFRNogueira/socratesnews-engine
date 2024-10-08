from bs4 import BeautifulSoup
import re

class Veja:

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
            contentBody = self.html.find('section', class_='content').find_all('p')
            for p in contentBody:
                content += p.get_text()
                content += "\n"
            content = re.sub(r'\s+', ' ', content).strip()
            return content
        except:
            return None


    def get_image(self):
        try:
            imageUrl = self.html.get('figure', class_='featured-media').find('img').get('src')
            imageText = self.html.find('figure', class_='featured-media').find('figcaption').find('spam').get_text()
            return imageUrl, imageText
        except:
            return None, None
