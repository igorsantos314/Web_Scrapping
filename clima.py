from bs4 import BeautifulSoup
import requests
import os, shutil

#EXEMPLOS
#print(soup.prettify())
#brasileirao = soup.find("div", class_="S2ILnf nCzB3b")
#print(soup.find("table", class_="infobox infobox_v2"))

class web_scrapping:

    def __init__(self):
        
        self.dict_dados = {}
        self.chaves = ["Municípios limítrofes", "Fundação", "Densidade", "Clima", "Altitude", "IDH", "PIB"]
        self.parametro_replace = ['muni_limi', 'fund_', 'dens_', 'clima_', 'altitude_', 'idh_', 'pib_']

        self.territorio = ""
        self.municipio = ""
        self.adm = ""
        self.transporte = ""
        self.distancia = ""

    def scrapping(self, link):
        html = requests.get(link).content

        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find("table", attrs={"class":"infobox infobox_v2"})

        texto_site = table.text
        self.topicos = texto_site.replace("\n\n", "\n}\n{\n").split("\n}\n{\n")

        for pos, i in enumerate(self.topicos):

            if "Municípios limítrofes" in i:
                self.dict_dados["Municípios limítrofes"] = self.topicos[pos+1]

            if "Densidade" in i:
                self.dict_dados["Densidade"] = self.topicos[pos+1]

            if "Clima" in i:
                self.dict_dados["Clima"] = self.topicos[pos+1]

            if "Altitude" in i:
                self.dict_dados["Altitude"] = self.topicos[pos+1]

            if "IDH" in i:
                self.dict_dados["IDH"] = self.topicos[pos+1]

            if "PIB" in i:
                self.dict_dados["PIB"] = self.topicos[pos+1]

            if "Fundação" in i:
                self.dict_dados["Fundação"] = self.topicos[pos+1]

            if "Aniversário" in i:
                self.dict_dados["Aniversário"] = self.topicos[pos+1]
    
    def substituir(self, cidade_titulo):
        #--- ARQUIVO TEMPLATE ---
        arq = open("Template/Template.html", "r", encoding = "utf-8")
        self.arq_str = arq.read().replace("titulo_para_mudar", cidade_titulo).replace(
            self.parametro_replace[0], 
            self.dict_dados[self.chaves[0]]).replace(
                self.parametro_replace[1], 
                self.dict_dados[self.chaves[1]]).replace(
                    self.parametro_replace[2], 
                    self.dict_dados[self.chaves[2]]).replace(
                        self.parametro_replace[3], 
                        self.dict_dados[self.chaves[3]]).replace(
                            self.parametro_replace[4], 
                            self.dict_dados[self.chaves[4]]).replace(
                                self.parametro_replace[5], 
                                self.dict_dados[self.chaves[5]]).replace(
                                    self.parametro_replace[6], 
                                    self.dict_dados[self.chaves[6]]).replace(
                                        "_linhas_dados_territorio", 
                                        self.territorio).replace(
                                            "_linhas_dados_municipio", self.municipio).replace(
                                                "_linhas_dados_adm",
                                                self.adm).replace(
                                                    "_linhas_dados_transporte",
                                                    self.transporte).replace(
                                                        "_linhas_dados_info_distancia",
                                                        self.distancia)

    def salvar(self, cidade):
        #--- CRIAR DIRETORIO DA CIDADE ---
        os.mkdir(cidade)

        #--- SALVAR ARQUIVO HTML---
        arq_html = open(cidade + "/" + cidade + ".html", "w", encoding="utf-8")
        arq_html.write(self.arq_str)
        arq_html.close()

        #--- SALVAR ARQUIVO CSS ---
        arq_css = open("Template/style.css", "r", encoding = "utf-8")
        arq_css_str = arq_css.read()

        arq_css_destino = open(cidade + "/style.css", "w", encoding="utf-8")
        arq_css_destino.write(arq_css_str)
        arq_css_destino.close()

    def start(self):
        cidade_titulo = input("Nome da Cidade Titulo: ")
        cidade_html =   input("Nome do Arquivo Html:  ")
        link =          input("Link do Wikipedia:     ")

        print('-------------------------------------')

        print('iniciando scrapping ...')
        self.scrapping(link)
        self.info_geral()

        print('carregando tamplate ...')
        self.substituir(cidade_titulo.upper())

        print('salvando novo site ...')
        self.salvar(cidade_html.title())

        print('\n ---> OK <--- ')

    def info_geral(self):

        html = requests.get("https://www.cidade-brasil.com.br/municipio-tururu.html").content
        soup = BeautifulSoup(html, 'html.parser')

        def info_territorio():
            territorio_corpo = soup.find("div", attrs={"id":"div_territorio"})
            territorio_table = territorio_corpo.find("table", attrs={})
            territorio_table_row = territorio_table.findAll("tr")

            rows = ""

            for i in territorio_table_row:
                str = i.prettify()

                if "Hora local" in str or "UTC" in str:
                    pass
                else:
                    rows += i.prettify()

            self.territorio = rows

        def info_municipio():
            municipio_corpo = soup.find("div", attrs={"id":"div_municipio"})
            municipio_table = municipio_corpo.find("table")
            municipio_table_row = municipio_table.findAll("tr")

            rows = ""

            for i in municipio_table_row:
                str = i.prettify()
                rows += str

            self.municipio = rows

        def info_adm():
            adm_corpo = soup.find("div", attrs={"id":"div_administracao"})
            adm_table = adm_corpo.find("table")
            adm_table_row = adm_table.findAll("tr")

            rows = ""

            for i in adm_table_row:
                str = i.prettify()

                if "Ver o resultado" in str:
                    pass
                
                else:
                    rows += str

            self.adm = rows

        def info_transporte():
            transporte_corpo = soup.find("div", attrs={"id":"div_transporte"})
            transporte_table = transporte_corpo.find("table")
            transporte_table_row = transporte_table.findAll("tr")

            rows = ""

            for i in transporte_table_row:
                str = i.prettify()
                rows += str

            self.transporte = rows

        def info_distancia():
            transporte_corpo = soup.find("div", attrs={"id":"div_distancia"})
            transporte_table = transporte_corpo.find("table")
            transporte_table_row = transporte_table.findAll("tr")

            rows = ""

            for i in transporte_table_row:
                str = i.prettify()
                rows += str

            self.distancia = rows

        # --- CHAMAR FUNÇÕES ---
        info_territorio()
        info_municipio()
        info_adm()
        info_transporte()
        info_distancia()

web_scrapping().start()
#
#for i in lista:
#    if "História" in i and "":
#        break
#    print(i)
