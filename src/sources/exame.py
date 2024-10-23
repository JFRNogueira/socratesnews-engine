from bs4 import BeautifulSoup
import re

class Exame:

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
            for p in self.html.find('section', class_="news-content-container").find_all('p'):
                content += p.get_text()
                content += "\n"
            content = re.sub(r'\s+', ' ', content).strip()
            return content
        except:
            return None


    def get_image(self):
        try:
            imageUrl = 'https://exame.com' + self.html.find('figure').find('img').get('src')
            imageText = self.html.find('figcaption').get_text()
            print(imageText)
            return imageUrl, imageText
        except:
            return None, None


