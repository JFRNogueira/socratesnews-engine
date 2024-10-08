import requests
from bs4 import BeautifulSoup


class MundoThemes:
    
    def __init__(self):
        self.themes = self.get_themes()


        
    def get_html(self, url):
        browsers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36"}
        html_content = requests.get(url, headers=browsers)
        soup = BeautifulSoup(html_content.text, 'html.parser')
        return soup


    
    def get_themes(self):
        soup = self.get_html("https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGx1YlY4U0JYQjBMVUpTR2dKQ1VpZ0FQAQ?hl=pt-BR&gl=BR&ceid=BR%3Apt-419")
        news_blocks = soup.find_all('a')
        result = []
        for nb in news_blocks:
            try:
                if nb.get('aria-label') == "Cobertura completa":
                    all_news = 'https://news.google.com' + nb.get('href')[1:]
                    result.append({'url': all_news})
            except:
                pass
        return result



