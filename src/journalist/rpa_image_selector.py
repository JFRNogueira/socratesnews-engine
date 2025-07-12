import requests
import re


# 1. Listar IDs das notícias que estão sem imagem
# 2. Buscar, para cada uma das notícias, as imagens disponíveis com seus respectivos textos
# 3. Indentificar imagem disponível baseado no texto


class RPAImageSelector:



    def __init__(self):
        self.news = []
        self.get_latest_news()
        self.filter_news()
        self.selectImage()
        


    def get_latest_news(self):
        try:
            for page in [1]:
                url = f'https://api-prod.jornalsocrates.com.br/api/news?page={page}'
                response = requests.get(url)
                if response.status_code != 200:
                    print(response.json())
                res = response.json()
                for n in res:
                    self.news.append({'newsId': n['newsId'], 'imageUrl': n['imageUrl']})
            return response.json()
        except Exception as e:
            print("Problema ao buscar notícia:", e)



    def filter_news(self):
        try:
            filtered_news = []
            for news in self.news:
                if news['imageUrl'] == 'https://images.unsplash.com/photo-1552012086-18eece80a2d9?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D':
                    filtered_news.append(news)
            
            self.news = filtered_news
        except Exception as e:
            print("Problema ao filtrar imagens:", e)
        
    
    
    def limpar_string(self, texto):
        texto = texto.strip()
        texto = re.sub(r'\s+', ' ', texto)
        return texto
        


    def get_news_references_images(self, newsId):
        try:
            url = f'https://api-prod.jornalsocrates.com.br/api/news/{newsId}'
            response = requests.get(url)
            if response.status_code != 200:
                print(response.json())
            res = response.json()
            references = res['referenceNews']
            references_with_image = []
            for r in references:
                if r['imageUrl'] != 'N/A' and r['imageText'] != 'N/A':
                    imageText_clean = self.limpar_string(r['imageText'])
                    references_with_image.append({'imageUrl': r['imageUrl'], 'imageText': r['imageText']})
            return references_with_image
        except Exception as e:
            print("Problema ao buscar referências para notícia:", e)



    def save_news_image(self, newsId, imageUrl, imageText):
        try:
            url = f'https://api-prod.jornalsocrates.com.br/api/news/{newsId}'
            payload = {
                "uid": 'jvfbEGdoKJYokMi4FgA3AFMI4tO2',
                "supportUid": 'jvfbEGdoKJYokMi4FgA3AFMI4tO2',
                'imageUrl': imageUrl, 
                'imageText': imageText,
            }
            response = requests.patch(url, json=payload)
            if response.status_code != 200:
                print(response.json())
            res = response.json()
            return res
        except Exception as e:
            print("Problema ao salvar imagem da notícia:", e)



    def selectImage(self):
        try:
            for n in self.news:
                newsId = n['newsId']
                # Chama o método passando o newsId como parâmetro
                references = self.get_news_references_images(newsId)
                selected = False
                for r in references:
                    if not selected:
                        pos = r['imageText'].lower().find('reprodução')
                        if pos != -1:
                            imageText = r['imageText'][pos:]
                            self.save_news_image(newsId, r['imageUrl'], imageText)
                            print(newsId)
                            print(r['imageUrl'])
                            print(imageText)
                            selected = True
        except Exception as e:
            print("Problema ao buscar imagem da notícia:", e)
            
            





# Se for main
if __name__ == "__main__":
    RPAImageSelector()





