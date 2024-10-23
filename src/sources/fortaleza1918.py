from bs4 import BeautifulSoup
import re

class Fortaleza1918:

    def __init__(self, url):
        self.url = url
        # self.suburls = self.get_suburls()
        self.html = self.get_html()
        self.title = self.get_title()
        self.text = self.get_text()


    def get_suburls(self):
        try:
            headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36"}
            response = requests.get(self.url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            all_hrefs = soup.find_all('a')
            urls = []
            for a in all_hrefs:
                href = a.get('href')
                if href is not None:
                    urls.append(href)
            return list(set(urls))
        except:
            return []


    def get_html(self):
        try:
            browsers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36"}
            page = requests.get(self.url, headers = browsers)
            resposta = page.text
            soup = BeautifulSoup(resposta, 'html.parser')
            return soup
        except:
            return None


    def get_title(self):
        try:
            title = self.html.find('h2', class_="elementor-heading-title").get_text()
            return title.strip()
        except:
            return None


    def get_text(self):
        try:
            content = ""
            for p in self.html.find('div', class_="elementor-widget-container").find_all('p'):
                content += p.get_text()
                content += "\n"
            content = re.sub(r'\s+', ' ', content).strip()
            return content
        except:
            return None
