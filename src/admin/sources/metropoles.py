from bs4 import BeautifulSoup
import re

class Metropoles:

    def __init__(self, html):
        self.html = html
        self.title = self.get_title()
        self.text = self.get_text()
        self.imageUrl, self.imageText = self.get_image()    


    def get_title(self):
        try:
            title = self.html.find('div', class_='HeaderNoticiaWrapper-sc-4exe2y-0').find('h1').get_text()
            return title.strip()
        except:
            return None


    def get_text(self):
        try:
            content = ""            
            contentBody = self.html.find('div', class_='ConteudoNoticiaWrapper__Artigo-sc-19fsm27-1').find_all('p')
            for p in contentBody:
                content += p.get_text()
                content += "\n"
            content = re.sub(r'\s+', ' ', content).strip()
            return content
        except:
            return None


    def get_image(self):
        try:
            image = self.html.find('div', class_='ImgDestaqueNoticiaWrapper-sc-1frrxvx-0')
            imageUrl = image.find('img').get('src')
            imageText = image.find('figcaption').get_text()
            return imageUrl, imageText
        except:
            return None, None
