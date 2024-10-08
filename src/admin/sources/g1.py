from bs4 import BeautifulSoup
import re

class G1:

    def __init__(self, html):
        self.html = html
        self.title = self.get_title()
        self.text = self.get_text()
        self.imageUrl, self.imageText = self.get_image()    


    def get_title(self):
        try:
            title = self.html.find('h1', class_='content-head__title').get_text()
            return title.strip()
        except:
            return None


    def get_text(self):
        try:
            content = ""            
            contentBody = self.html.find('div', class_=['mc-article-body', 'cb-summary-container']).find_all('p')
            for p in contentBody:
                content += p.get_text()
                content += "\n"
            content = re.sub(r'\s+', ' ', content).strip()
            return content
        except:
            return None


    def get_image(self):
        try:
            image = self.html.find('figure', class_='content-media-figure')
            imageUrl = image.find('amp-img').get('src')
            imageText = image.find('amp-img').get('alt')
            return imageUrl, imageText
        except:
            return None, None
