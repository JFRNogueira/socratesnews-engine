from bs4 import BeautifulSoup
import re

class CorreioDoPovo:

    def __init__(self, html):
        self.html = html
        self.title = self.get_title()
        self.text = self.get_text()
        self.imageUrl, self.imageText = self.get_image()


    def get_title(self):
        try:
            title = self.html.find('h1', class_="article__headline container").get_text()
            return title.strip()
        except:
            return None


    def get_text(self):
        try:
            content = ""
            for p in self.html.find('div', class_='article__body').find_all('p'):
                content += p.get_text()
                content += "\n"
            content = re.sub(r'\s+', ' ', content).strip()
            return content
        except:
            return None


    def get_image(self):
        try:
            image = self.html.find('div', class_='image')
            imageUrl = image.get('img').get('src')
            imageText = self.html.find('span', class_='image-byline').find('span').get_text()
            return imageUrl, imageText
        except:
            return None, None