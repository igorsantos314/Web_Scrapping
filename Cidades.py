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

        self.historia_geral = ""

        self.CURR_DIR = os.getcwd()

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
                                                        self.distancia).replace(
                                                            "conteudo_historia", self.historia_geral
                                                        )

    def salvar(self, cidade):
        dir = self.CURR_DIR + "/pages/"

        #--- CRIAR DIRETORIO DA CIDADE ---
        if os.path.exists(dir + cidade):
            shutil.rmtree(dir + cidade, ignore_errors=True)

        os.mkdir(dir + cidade)

        #--- SALVAR ARQUIVO HTML---
        arq_html = open(dir + cidade + "/" + cidade + ".html", "w", encoding="utf-8")
        arq_html.write(self.arq_str)
        arq_html.close()

    def start(self):
        #cidade_titulo = input("Nome da Cidade Titulo: ")
        #cidade_html =   input("Nome do Arquivo Html:  ")
        #link =          input("Link do Wikipedia:     ")

        dict_cidades = {    1:['Graça', 'Graca', 'https://pt.wikipedia.org/wiki/Graça_(Ceará)'],
                            2:['Tururu', 'Tururu', 'https://pt.wikipedia.org/wiki/Tururu'],
                            3:['Itapiúna', 'Itapiuna', 'https://pt.wikipedia.org/wiki/Itapiúna'],
                            4:['Abaiara', 'Abaiara', 'https://pt.wikipedia.org/wiki/Abaiara'],
                            5:['Pindoretama', 'Pindoretama', 'https://pt.wikipedia.org/wiki/Pindoretama'],
                            6:['Orós', 'Oros', 'https://pt.wikipedia.org/wiki/Orós'],
                            7:['Martinópole', 'Martinopole', 'https://pt.wikipedia.org/wiki/Martinópole'],
                            8:['Fortaleza', 'Fortaleza', 'https://pt.wikipedia.org/wiki/Fortaleza'],
                            9:['Caririaçu', 'Caririacu', 'https://pt.wikipedia.org/wiki/Caririaçu'],
                            10:['General Sampaio', 'General Sampaio', 'https://pt.wikipedia.org/wiki/General_Sampaio']
                        }

        for i in dict_cidades:
            cidade_titulo = dict_cidades[i][0]
            cidade_html = dict_cidades[i][1]
            link = dict_cidades[i][2]

            print('\n-------------------------------------')

            print('iniciando scrapping ...')
            self.scrapping(link)
            self.info_geral(cidade_html)
            self.historia(cidade_html.lower().replace(' ', '-'))

            print('carregando tamplate ...')
            self.substituir(cidade_titulo.upper())

            print('salvando novo site ...')
            self.salvar(cidade_html.title().replace(' ', '_'))

            print(f'\n ---> CIDADE: {cidade_titulo} OK!<--- ')

    def historia(self, cidade):
        html = requests.get(f"https://cidades.ibge.gov.br/brasil/ce/{cidade}/historico").content
        soup = BeautifulSoup(html, 'html.parser')

        hist_titulo = soup.findAll("h2", attrs={"class":"hist__titulo"})
        historia_texto = soup.findAll("div", attrs={"class":"hist__texto"})

        rows = ''

        for pos, i in enumerate(historia_texto):
            rows += "<h2 style>" + hist_titulo[pos].text + "</h2>"
            rows += i.prettify()

        self.historia_geral = rows

    def info_geral(self, cidade):

        html = requests.get(f"https://www.cidade-brasil.com.br/municipio-{cidade}.html").content
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

            self.municipio = replace_coluna(municipio_table_row)

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

            self.transporte = replace_link(transporte_table_row)

        def info_distancia():
            transporte_corpo = soup.find("div", attrs={"id":"div_distancia"})
            transporte_table = transporte_corpo.find("table")
            transporte_table_row = transporte_table.findAll("tr")

            self.distancia = replace_link(transporte_table_row)

        def replace_link(table_row):

            links = []
            rows = ""

            for i in table_row:
                str = i.prettify()

                for pos, i in enumerate(str):
                    if i == '<' and str[pos+1] == 'a':
                        cont = pos
                        link = ''

                        while True:
                            if str[cont] == '>':
                                link += str[cont]
                                links.append(link)
                                break
                                
                            else:
                                link += str[cont]
                                cont += 1

                rows += str

            #SUBSTITUIR 
            for lk in links:
                rows = rows.replace(lk, "")

            return rows.replace("</a>", "")

        def replace_coluna(table_row):

            links = []
            rows = ""

            for i in table_row:
                str = i.prettify()
                
                for pos, i in enumerate(str):
                    if i == '<' and str[pos+1] == 't' and str[pos+2] == 'd' and str[pos+13] == '6':
                        cont = pos
                        link = ''
                        pass_td = True

                        while True:
                            if str[cont-4] == '<' and str[cont-3] == '/' and str[cont-2] == 't' and str[cont-1] == 'd' and str[cont] == '>':
                                link += str[cont]
                                links.append(link)

                                if pass_td:
                                    pass_td = False

                                elif pass_td == False:
                                    break

                            else:
                                link += str[cont]
                                cont += 1

                rows += str

            #SUBSTITUIR 
            for lk in links:
                rows = rows.replace(lk, "")

            return rows.replace("</a>", "")

        # --- CHAMAR FUNÇÕES ---
        info_territorio()
        info_municipio()
        info_adm()
        info_transporte()
        info_distancia()


web_scrapping().start()
