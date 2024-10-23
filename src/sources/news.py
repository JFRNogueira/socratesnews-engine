import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from sources.agenciabrasil import AgenciaBrasil
from sources.banduol import BandUol
from sources.bbc import BBC
from sources.bolavip import BolaVip
from sources.boluol import BolUol
from sources.cartacapital import CartaCapital
from sources.cnnbrasil import CnnBrasil
from sources.correio_braziliense import CorreioBraziliense
from sources.correio_do_povo import CorreioDoPovo
from sources.crusoe import Crusoe
from sources.dw import DW
from sources.espn import Espn
from sources.estadao import Estadao
from sources.exame import Exame
from sources.folhauol import FolhaUol
from sources.g1 import G1
from sources.game_vicio import GameVicio
from sources.gazeta_do_povo import GazetaDoPovo
from sources.gzh import GZH
from sources.istoe import Istoe
from sources.infomoney import InfoMoney
from sources.jovempan import JovemPan
from sources.metropoles import Metropoles
from sources.meups import MeuPS
from sources.ndmais import NDMais
from sources.oglobo import OGlobo
from sources.olhardigital import OlharDigital
from sources.o_tempo import OTempo
from sources.o_vicio import OVicio
from sources.poder360 import Poder360
from sources.r7 import R7
from sources.series_do_momento import SeriesDoMomento
from sources.tecmundo import TecMundo
from sources.terra import Terra
from sources.trivela import Trivela
from sources.tudo_celular import TudoCelular
from sources.ultimosegundo import UltimoSegundo
from sources.uol import Uol
from sources.vasco import Vasco
from sources.veja import Veja
from sources.viomundo import ViOMundo
from sources.windows_club import WindowsClub



class News:

    def __init__(self, url):
        self.url = url
        self.soup = self.get_html()
        self.source, self.newsdata = self.get_data()
        self.title, self.text, self.imageUrl, self.imageText = self.split_data()



    def get_html(self):
        browsers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36"}
        html_content = requests.get(self.url, headers = browsers, timeout=20)
        text = html_content.content.decode('utf-8', errors='ignore')
        soup = BeautifulSoup(text, 'html.parser')
        return soup



    def get_data(self):
        if 'agenciabrasil.ebc.com.br' in self.url:
            newsdata = AgenciaBrasil(self.soup)
            return 'agenciabrasil', newsdata
        if 'band.uol.com.br' in self.url:
            newsdata = BandUol(self.soup)
            return 'banduol', newsdata
        if 'bbc.com' in self.url:
            newsdata = BBC(self.soup)
            return 'bbc', newsdata
        if 'bolavip.com' in self.url:
            newsdata = BolaVip(self.soup)
            return 'bolavip', newsdata
        if 'bol.uol.com.br' in self.url:
            newsdata = BolUol(self.soup)
            return 'boluol', newsdata
        if 'cartacapital.com.br' in self.url:
            newsdata = CartaCapital(self.soup)
            return 'cartacapital', newsdata
        if 'cnnbrasil.com.br' in self.url:
            newsdata = CnnBrasil(self.soup)
            return 'cnnbrasil', newsdata
        if 'correiobraziliense.com.br' in self.url:
            newsdata = CorreioBraziliense(self.soup)
            return 'correiobraziliense', newsdata
        if 'correiodopovo.com.br' in self.url:
            newsdata = CorreioDoPovo(self.soup)
            return 'correiodopovo', newsdata
        if 'crusoe.com.br' in self.url:
            newsdata = Crusoe(self.soup)
            return 'crusoe', newsdata
        if 'dw.com' in self.url:
            newsdata = DW(self.soup)
            return 'dw', newsdata
        if 'espn.com.br' in self.url:
            newsdata = Espn(self.soup)
            return 'espn', newsdata
        if 'estadao.com.br' in self.url:
            newsdata = Estadao(self.soup)
            return 'estadao', newsdata
        if 'exame.com' in self.url:
            newsdata = Exame(self.soup)
            return 'exame', newsdata
        if 'folha.uol.com.br' in self.url:
            newsdata = FolhaUol(self.soup)
            return 'folhauol', newsdata
        if 'gazetadopovo.com.br' in self.url:
            newsdata = GazetaDoPovo(self.soup)
            return 'gazetadopovo', newsdata
        if 'ge.globo.com' in self.url:
            newsdata = G1(self.soup)
            return 'geglobo', newsdata
        if 'g1.globo.com' in self.url:
            newsdata = G1(self.soup)
            return 'g1globo', newsdata
        if 'gamevicio.com' in self.url:
            newsdata = GameVicio(self.soup)
            return 'gamevicio', newsdata
        if 'gauchazh.clicrbs.com.br' in self.url:
            newsdata = GZH(self.soup)
            return 'gzh', newsdata
        if 'istoe.com.br' in self.url:
            newsdata = Istoe(self.soup)
            return 'istoe', newsdata
        if 'infomoney.com.br' in self.url:
            newsdata = InfoMoney(self.soup)
            return 'infomoney', newsdata
        if 'jovempan.com.br' in self.url:
            newsdata = JovemPan(self.soup)
            return 'jovempan', newsdata
        if 'metropoles.com' in self.url:
            newsdata = Metropoles(self.soup)
            return 'metropoles', newsdata
        if 'meups.com.br' in self.url:
            newsdata = MeuPS(self.soup)
            return 'meups', newsdata
        if 'ndmais.com.br' in self.url:
            newsdata = NDMais(self.soup)
            return 'ndmais', newsdata
        if 'oglobo.globo.com' in self.url:
            newsdata = OGlobo(self.soup)
            return 'oglobo', newsdata
        if 'olhardigital.com.br' in self.url:
            newsdata = OlharDigital(self.soup)
            return 'olhardigital', newsdata
        if 'otempo.com.br' in self.url:
            newsdata = OTempo(self.soup)
            return 'otempo', newsdata
        if 'poder360.com.br' in self.url:
            newsdata = Poder360(self.soup)
            return 'poder360', newsdata
        if 'r7.com' in self.url:
            newsdata = R7(self.soup)
            return 'r7', newsdata
        if 'seriesdomomento.com.br' in self.url:
            newsdata = SeriesDoMomento(self.soup)
            return 'seriesdomomento', newsdata
        if 'tecmundo.com.br' in self.url:
            newsdata = TecMundo(self.soup)
            return 'tecmundo', newsdata
        if 'terra.com.br' in self.url:
            newsdata = Terra(self.soup)
            return 'terra', newsdata
        if 'trivela.com.br' in self.url:
            newsdata = Trivela(self.soup)
            return 'trivela', newsdata
        if 'tudocelular.com' in self.url:
            newsdata = TudoCelular(self.soup)
            return 'tudocelular', newsdata
        if 'ultimosegundo.ig.com.br' in self.url:
            newsdata = UltimoSegundo(self.soup)
            return 'ultimosegundo', newsdata
        if 'noticias.uol.com.br' in self.url:
            newsdata = Uol(self.soup)
            return 'uol', newsdata
        if 'vasco.com.br' in self.url:
            newsdata = Vasco(self.soup)
            return 'vasco', newsdata
        if 'veja.abril.com.br' in self.url:
            newsdata = Veja(self.soup)
            return 'veja', newsdata
        if 'viomundo.com.br' in self.url:
            newsdata = ViOMundo(self.soup)
            return 'viomundo', newsdata
        if 'windowsclub.com.br' in self.url:
            newsdata = WindowsClub(self.soup)
            return 'windowsclub', newsdata
        with open('src/admin/bot_jornalista/not_found_url_reader.csv', mode="a", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["ts", "url"])
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow({"ts": datetime.now().isoformat(), "url": self.url})
        return 'outro', None



    def split_data(self):
        if self.source != 'outro':
            nd = self.newsdata
            return nd.title, nd.text, nd.imageUrl, nd.imageText
        else:
            return None, None, None, None