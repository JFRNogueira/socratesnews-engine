import shutil
import json
import os
import streamlit as st

from journalist.previsoes_sec import HoroscopoSec


def get_full_date_str():
    return 'Terça-feira, 21 de agosto de 2024'  # TODO: Implementar função

def get_edition_year():
    return '1'  # TODO: Implementar função

def get_edition_number():
    return '1'  # TODO: Implementar função

def get_page_number():
    return st.session_state['printed_version_page_number'].replace('Página ', '')

def get_news_header():
    return st.session_state['printed_version_page_title']



class SrcBuilder:

    def get_layout(self):
        return st.session_state['printed_version_layout']
    
    def get_page(self):
        return st.session_state['printed_version_page_number'].replace('Página ', '')
    
    def create_layout(self):
        layout = st.session_state['printed_version_layout']
        st.markdown(f'Layout selecionado: {layout}')
    
    def get_header(self):
        if self.get_page() == 1:
            return r'\frontpageheaderVA{get_edition_year()}{get_edition_number()}{get_full_date_str()}'
        else:
            return f'\\headerVA{get_edition_year()}{get_edition_number()}{get_full_date_str()}'

    
    def model1(self):
        self.create_layout()
        shutil.copyfile(f'{os.getcwd()}/src/printedversion/pages/params/page_src.tex', f'{os.getcwd()}/src/printedversion/pages/{self.get_page()}/page_src.tex')
        
        tex_params = json.load(open(f'{os.getcwd()}/src/printedversion/pages/{self.get_page()}/src.json', 'r', encoding='utf-8'))
        replacements = [
            {"from": '###get_edition_year()###', "to": get_edition_year()},
            {"from": '###get_edition_number()###', "to": get_edition_number()},
            {"from": '###get_full_date_str()###', "to": get_full_date_str()},
            {"from": '###image1###', "to": tex_params['news'][0]['imagePath']},
            {"from": '###h1###', "to": tex_params['news'][0]['title']},
            {"from": '###preamble1###', "to": tex_params['news'][0]['summary']},
            {"from": '###text1###', "to": tex_params['news'][0]['text']},
            {"from": '###image2###', "to": tex_params['news'][1]['imagePath']},
            {"from": '###h2###', "to": tex_params['news'][1]['title']},
            {"from": '###preamble2###', "to": tex_params['news'][1]['summary']},
            {"from": '###text2###', "to": tex_params['news'][1]['text']},
            {"from": '###image3###', "to": tex_params['news'][2]['imagePath']},
            {"from": '###h3###', "to": tex_params['news'][2]['title']},
            {"from": '###preamble3###', "to": tex_params['news'][2]['summary']},
            {"from": '###text3###', "to": tex_params['news'][2]['text']},
            {"from": '###image4###', "to": tex_params['news'][3]['imagePath']},
            {"from": '###h4###', "to": tex_params['news'][3]['title']},
            {"from": '###preamble4###', "to": tex_params['news'][3]['summary']},
            {"from": '###text4###', "to": tex_params['news'][3]['text']}
        ]
        with open(f'./src/printedversion/pages/params/{self.get_page()}.txt', 'r', encoding='utf-8') as f:
            tex_template = f.read()
            f.close()
        
        for replacement in replacements:
            tex_template = tex_template.replace(replacement['from'], replacement['to'])
        
        # abrir o arquivo .tex
        with open('./src/printedversion/pages/1/page_src.tex', 'a', encoding='utf-8') as f:
            f.writelines(tex_template)
            f.close()



    def model2(self):
        shutil.copyfile(f'{os.getcwd()}/src/printedversion/pages/params/page_src.tex', f'{os.getcwd()}/src/printedversion/pages/{self.get_page()}/page_src.tex')
        
        tex_params = json.load(open(f'{os.getcwd()}/src/printedversion/pages/{self.get_page()}/src.json', 'r', encoding='utf-8'))
        tex_template = '\\begin{document}\n\n'
        tex_template += '\\frontpageheaderVA' + 'impar{' if self.get_page() % 2 == 1 else 'par{' + get_edition_year() + '}{' + get_edition_number() + '}{' + get_full_date_str() + '}{' + get_page_number() + '}{' + get_news_header() + '}\n\n'
        tex_template += '\\thispagestyle{empty}\n\n'
        tex_template += '\\newspageVAone  {' + tex_params['news'][0]['imagePath'] + '}{' + tex_params['news'][0]['title'] + '}{' + tex_params['news'][0]['summary'] + '}{' + tex_params['news'][0]['text'] + '}\n\n'
        tex_template += '\\newspageVAtwo  {' + tex_params['news'][1]['imagePath'] + '}{' + tex_params['news'][1]['title'] + '}{' + tex_params['news'][1]['summary'] + '}{' + tex_params['news'][1]['text'] + '}\n\n'
        tex_template += '\\newspageVAthree{' + tex_params['news'][2]['imagePath'] + '}{' + tex_params['news'][2]['title'] + '}{' + tex_params['news'][2]['summary'] + '}{' + tex_params['news'][2]['text'] + '}\n\n'
        tex_template += '\\newspagefooterVA\n\n'        
        tex_template += '\\end{document}\n\n'
        
        with open(f'./src/printedversion/pages/{get_page_number()}/page_src.tex', 'a', encoding='utf-8') as f:
            f.writelines(tex_template)
            f.close()



    def model3(self):
        shutil.copyfile(f'{os.getcwd()}/src/printedversion/pages/params/page_src.tex', f'{os.getcwd()}/src/printedversion/pages/{self.get_page()}/page_src.tex')
        
        tex_params = json.load(open(f'{os.getcwd()}/src/printedversion/pages/{self.get_page()}/src.json', 'r', encoding='utf-8'))
        tex_template = '\\begin{document}\n\n'
        tex_template += '\\frontpageheaderVA' + 'impar{' if self.get_page() % 2 == 1 else 'par{' + get_edition_year() + '}{' + get_edition_number() + '}{' + get_full_date_str() + '}{' + get_page_number() + '}{' + get_news_header() + '}\n\n'
        tex_template += '\\thispagestyle{empty}\n\n'
        tex_template += '\\forecastsections\n\n'
        
        tex_template += '\\forecasthoroscope{0}{0}' + f'{"Áries - 21-mar a 20-abr"}', f'{HoroscopoSec().create_one_daily_horoscope("aries")}'
        tex_template += '\\forecasthoroscope{0}{1}' + f'{"Touro - 21-abr a 20-mai"}', f'{HoroscopoSec().create_one_daily_horoscope("touro")}'
        tex_template += '\\forecasthoroscope{0}{2}' + f'{"Gêmeos - 21-mai a 20-jun"}', f'{HoroscopoSec().create_one_daily_horoscope("gemeos")}'
        tex_template += '\\forecasthoroscope{0}{3}' + f'{"Câncer - 21-jun a 21-jul"}', f'{HoroscopoSec().create_one_daily_horoscope("cancer")}'
        tex_template += '\\forecasthoroscope{0}{4}' + f'{"Leão - 22-jul a 22-ago"}', f'{HoroscopoSec().create_one_daily_horoscope("leao")}'
        tex_template += '\\forecasthoroscope{0}{5}' + f'{"Virgem - 23-ago a 22-set"}', f'{HoroscopoSec().create_one_daily_horoscope("virgem")}'
        tex_template += '\\forecasthoroscope{1}{0}' + f'{"Libra - 23-set a 22-out"}', f'{HoroscopoSec().create_one_daily_horoscope("libra")}'
        tex_template += '\\forecasthoroscope{1}{1}' + f'{"Escorpião - 23-out a 21-nov"}', f'{HoroscopoSec().create_one_daily_horoscope("escorpiao")}'
        tex_template += '\\forecasthoroscope{1}{2}' + f'{"Sagitário - 22-nov a 21-dez"}', f'{HoroscopoSec().create_one_daily_horoscope("sagitario")}'
        tex_template += '\\forecasthoroscope{1}{3}' + f'{"Capricórnio - 22-dez a 20-jan"}', f'{HoroscopoSec().create_one_daily_horoscope("capricornio")}'
        tex_template += '\\forecasthoroscope{1}{4}' + f'{"Aquário - 21-jan a 19-fev"}', f'{HoroscopoSec().create_one_daily_horoscope("aquario")}'
        tex_template += '\\forecasthoroscope{1}{5}' + f'{"Peixes - 20-fev a 20-mar"}', f'{HoroscopoSec().create_one_daily_horoscope("peixes")}'
        
        tex_template += '\\end{document}\n\n'
        
        with open(f'./src/printedversion/pages/{get_page_number()}/page_src.tex', 'a', encoding='utf-8') as f:
            f.writelines(tex_template)
            f.close()




