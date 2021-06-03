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
        self.chaves = ["Municípios limítrofes", "Fundação", "População total", "Densidade", "Clima", "Altitude", "IDH", "PIB", "Área total"]
        self.parametro_replace = ['muni_limi', 'fund_', 'pop_total', 'dens_', 'clima_', 'altitude_', 'idh_', 'pib_', 'area_total']

    def scrapping(self, link):
        html = requests.get(link).content

        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find("table", attrs={"class":"infobox infobox_v2"})

        texto_site = table.text
        self.topicos = texto_site.replace("\n\n", "\n}\n{\n").split("\n}\n{\n")

        for pos, i in enumerate(self.topicos):

            if "Municípios limítrofes" in i:
                self.dict_dados["Municípios limítrofes"] = self.topicos[pos+1]

            if "Prefeito(a)" in i:
                self.dict_dados["Prefeito"] = self.topicos[pos+1]

            if "População total" in i:
                self.dict_dados["População total"] = self.topicos[pos+1]

            if "Área total" in i:
                self.dict_dados["Área total"] = self.topicos[pos+1]

            if "Densidade" in i:
                self.dict_dados["Densidade"] = self.topicos[pos+1]

            if "Clima" in i:
                self.dict_dados["Clima"] = self.topicos[pos+1]

            if "Altitude" in i:
                self.dict_dados["Altitude"] = self.topicos[pos+1]

            if "IDH" in i:
                self.dict_dados["IDH"] = self.topicos[pos+1]

            if "Gini" in i:
                self.dict_dadosGini = self.topicos[pos+1]

            if "PIB" in i:
                self.dict_dados["PIB"] = self.topicos[pos+1]

            if "Fundação" in i:
                self.dict_dados["Fundação"] = self.topicos[pos+1]

            if "Aniversário" in i:
                self.dict_dados["Aniversário"] = self.topicos[pos+1]
    
    def substituir(self, cidade_titulo):
        #--- ARQUIVO TEMPLATE ---
        arq = open("Template/Template.html", "r", encoding = "utf-8")
        self.arq_str = arq.read().replace("titulo_para_mudar", cidade_titulo).replace(self.parametro_replace[0], self.dict_dados[self.chaves[0]]).replace(self.parametro_replace[1], self.dict_dados[self.chaves[1]]).replace(self.parametro_replace[2], self.dict_dados[self.chaves[2]]).replace(self.parametro_replace[3], self.dict_dados[self.chaves[3]]).replace(self.parametro_replace[4], self.dict_dados[self.chaves[4]]).replace(self.parametro_replace[5], self.dict_dados[self.chaves[5]]).replace(self.parametro_replace[6], self.dict_dados[self.chaves[6]]).replace(self.parametro_replace[7], self.dict_dados[self.chaves[7]]).replace(self.parametro_replace[8], self.dict_dados[self.chaves[8]])

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

        print('carregando tamplate ...')
        self.substituir(cidade_titulo.upper())

        print('salvando novo site ...')
        self.salvar(cidade_html.title())

        print('\n ---> OK <--- ')

#web_scrapping().start()
html = requests.get("https://pt.wikipedia.org/wiki/Fortaleza").content
soup = BeautifulSoup(html, 'html.parser')

historia = soup.find("div", attrs={"class":"mw-parser-output"})
lista = historia.text.split("\n")

arq = open("test.html", "w", encoding="utf-8")
arq.write(soup.prettify())
arq.close()

#
#for i in lista:
#    if "História" in i and "":
#        break
#    print(i)
