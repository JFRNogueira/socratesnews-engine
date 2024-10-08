from bs4 import BeautifulSoup
import re

class Folha:

    def __init__(self, base_url='https://www.uol.com.br/'):
        self.base_url = base_url
    
    def yesterday_url_str(self):
        meses_abreviados = {
            1: "jan",
            2: "fev",
            3: "mar",
            4: "abr",
            5: "mai",
            6: "jun",
            7: "jul",
            8: "ago",
            9: "set",
            10: "out",
            11: "nov",
            12: "dez"
        }
        ontem = datetime.now() - timedelta(days=1)
        data_formatada = f"{ontem.day}.{meses_abreviados[ontem.month]}.{ontem.year}"
        return data_formatada

    def yesterday_url_str_month(self):
        ontem = datetime.now() - timedelta(days=1)
        data_formatada = ontem.strftime('/%Y/%m/')
        return data_formatada


    def getUrls(self, url, only_yesterday_month=True):
        try:
            headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36"}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            all_hrefs = soup.find_all('a', class_='c-headline__url') + soup.find_all('a', class_='c-main-headline__url')
            urls = []
            for a in all_hrefs:
                href = a.get('href')
                if href is not None:
                    if only_yesterday_month and self.yesterday_url_str_month() in href:
                        urls.append(href)
                    elif not only_yesterday_month:
                        urls.append(href)
            return list(set(urls))
        except:
            return []


    def getNewsData(self, url, only_yesterday=True):
        try:
            headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36"}
            page = requests.get(url, headers = headers)
            
            resposta = page.text
            soup = BeautifulSoup(resposta, 'html.parser')

            title = soup.find('h1', class_="c-content-head__title") or soup.find('h1', class_="news__title") 
            title = str_cleasing(title.get_text()).strip()
            
            timestamp = soup.find('time', itemprop='datePublished')
            isYesterday = self.yesterday_url_str() in timestamp
            
            content = ""
            contentHtml = soup.find('div', class_="c-news__body") or soup.find('div', class_="news__content")
            for c in contentHtml.find_all('p'):
                content += c.get_text()
                content = str_cleasing(content)
                content += '\n'
            
            if only_yesterday and not isYesterday:
                return None
                
            return {
                "url": url,
                "title": title,
                "content": content
            }
        except:
            return None
