from bs4 import BeautifulSoup
import requests
import os, shutil

class web_scrapping:

    def __init__(self):
        
        self.dict_dados = {}
        self.chaves = ["Municípios limítrofes", "Fundação", "Clima", "IDH", "PIB"]
        self.parametro_replace = ['muni_limi', 'fund_', 'clima_', 'idh_', 'pib_']

        self.territorio = ""
        self.municipio = ""
        self.adm = ""
        self.transporte = ""
        self.distancia = ""

        self.historia_geral = ""
        self.mapa = ""

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

            if "Clima" in i:
                self.dict_dados["Clima"] = self.topicos[pos+1]

            if "IDH" in i:
                self.dict_dados["IDH"] = self.topicos[pos+1]

            if "PIB" in i:
                self.dict_dados["PIB"] = self.topicos[pos+1]

            if "Fundação" in i:
                self.dict_dados["Fundação"] = self.topicos[pos+1]
    
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
                                        "_linhas_dados_territorio", 
                                        self.territorio).replace(
                                            "_linhas_dados_municipio", self.municipio).replace(
                                                "_linhas_dados_adm",
                                                self.adm).replace(
                                                    "_linhas_dados_transporte",
                                                    self.transporte).replace(
                                                        "_linhas_dados_info_distancia",
                                                        self.distancia).replace(
                                                                "_mapa",
                                                                self.mapa)

    def salvar(self, cidade):
        dir = self.CURR_DIR + "/pages/"

        #--- CRIAR DIRETORIO DA CIDADE ---
        if os.path.exists(dir + cidade):
            shutil.rmtree(dir + cidade, ignore_errors=True)

        os.mkdir(dir + cidade)
        os.mkdir(dir + cidade + "/src")

        #--- SALVAR ARQUIVO HTML---
        arq_html = open(dir + cidade + "/" + cidade + ".html", "w", encoding="utf-8")
        arq_html.write(self.arq_str)
        arq_html.close()

    def start(self):

        dict_cidades = {    1:['Graça', 'Graca', 'https://pt.wikipedia.org/wiki/Graça_(Ceará)', '<iframe src="https://www.google.com/maps/embed?pb=!1m28!1m12!1m3!1d1019018.313935277!2d-40.20152964138334!3d-3.90816767391178!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!4m13!3e6!4m5!1s0x794dc5c69df176f%3A0xee453f8e3d4c8715!2zR3Jhw6dhLCBDRQ!3m2!1d-4.0445958!2d-40.7493893!4m5!1s0x7c74c3f464c783f%3A0x4661c60a0c6b37ca!2sFortaleza%20-%20CE!3m2!1d-3.7327203!2d-38.5270134!5e0!3m2!1spt-BR!2sbr!4v1622936526686!5m2!1spt-BR!2sbr" width="100%" height="600" style="border:0;" allowfullscreen="" loading="lazy"></iframe>'],
                            2:['Tururu', 'Tururu', 'https://pt.wikipedia.org/wiki/Tururu', '<iframe src="https://www.google.com/maps/embed?pb=!1m28!1m12!1m3!1d509649.3812065502!2d-39.262466147486066!3d-3.6701102885158026!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!4m13!3e6!4m5!1s0x7c05b8e7a8306d5%3A0xe67963c551b6c20d!2sTururu%2C%20CE!3m2!1d-3.5982866!2d-39.4336292!4m5!1s0x7c74c3f464c783f%3A0x4661c60a0c6b37ca!2sFortaleza%20-%20CE!3m2!1d-3.7327203!2d-38.5270134!5e0!3m2!1spt-BR!2sbr!4v1622936594658!5m2!1spt-BR!2sbr" width="100%" height="600" style="border:0;" allowfullscreen="" loading="lazy"></iframe>'],
                            3:['Itapiúna', 'Itapiuna', 'https://pt.wikipedia.org/wiki/Itapiúna', '<iframe src="https://www.google.com/maps/embed?pb=!1m28!1m12!1m3!1d509359.5623659899!2d-38.97988034528306!3d-4.1471167000857125!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!4m13!3e6!4m5!1s0x7bedc5cf0323a73%3A0x8f6bfaa91c1dded3!2zSXRhcGnDum5hLCBDRQ!3m2!1d-4.5629728!2d-38.9210924!4m5!1s0x7c74c3f464c783f%3A0x4661c60a0c6b37ca!2sFortaleza%20-%20CE!3m2!1d-3.7327203!2d-38.5270134!5e0!3m2!1spt-BR!2sbr!4v1622936617106!5m2!1spt-BR!2sbr" width="100%" height="600" style="border:0;" allowfullscreen="" loading="lazy"></iframe>'],
                            4:['Abaiara', 'Abaiara', 'https://pt.wikipedia.org/wiki/Abaiara', '<iframe src="https://www.google.com/maps/embed?pb=!1m28!1m12!1m3!1d2033252.3251171834!2d-39.30731782928747!3d-5.537932337382022!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!4m13!3e6!4m5!1s0x7a1691bc8534507%3A0x62a0f764730ab5e5!2sAbaiara%2C%20CE!3m2!1d-7.346188799999999!2d-39.035626!4m5!1s0x7c74c3f464c783f%3A0x4661c60a0c6b37ca!2sFortaleza%20-%20CE!3m2!1d-3.7327203!2d-38.5270134!5e0!3m2!1spt-BR!2sbr!4v1622936667857!5m2!1spt-BR!2sbr" width="100%" height="600" style="border:0;" allowfullscreen="" loading="lazy"></iframe>'],
                            5:['Pindoretama', 'Pindoretama', 'https://pt.wikipedia.org/wiki/Pindoretama', '<iframe src="https://www.google.com/maps/embed?pb=!1m28!1m12!1m3!1d254762.46340218477!2d-38.55636315694886!3d-3.8821229177952796!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!4m13!3e6!4m5!1s0x7b89f655b8bc1e1%3A0x98d41b130b6bc0e8!2sPindoretama%2C%20CE!3m2!1d-4.0304585!2d-38.3036892!4m5!1s0x7c74c3f464c783f%3A0x4661c60a0c6b37ca!2sFortaleza%20-%20CE!3m2!1d-3.7327203!2d-38.5270134!5e0!3m2!1spt-BR!2sbr!4v1622936688114!5m2!1spt-BR!2sbr" width="100%" height="600" style="border:0;" allowfullscreen="" loading="lazy"></iframe>'],
                            6:['Orós', 'Oros', 'https://pt.wikipedia.org/wiki/Orós', '<iframe src="https://www.google.com/maps/embed?pb=!1m28!1m12!1m3!1d2035063.3883944156!2d-40.04264679233758!3d-4.983938465501245!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!4m13!3e6!4m5!1s0x7a34682cad6d325%3A0x9fb5b0754767a20b!2zT3LDs3MsIENF!3m2!1d-6.2446364!2d-38.915602199999995!4m5!1s0x7c74c3f464c783f%3A0x4661c60a0c6b37ca!2sFortaleza%20-%20CE!3m2!1d-3.7327203!2d-38.5270134!5e0!3m2!1spt-BR!2sbr!4v1622936713323!5m2!1spt-BR!2sbr" width="100%" height="600" style="border:0;" allowfullscreen="" loading="lazy"></iframe>'],
                            7:['Martinópole', 'Martinopole', 'https://pt.wikipedia.org/wiki/Martinópole', '<iframe src="https://www.google.com/maps/embed?pb=!1m28!1m12!1m3!1d1019162.7620490495!2d-40.173057897703416!3d-3.7874199824842987!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!4m13!3e6!4m5!1s0x7ebad968549f529%3A0x5887ed1405d37e60!2sMartin%C3%B3pole%2C%20CE!3m2!1d-3.2242659999999996!2d-40.6954624!4m5!1s0x7c74c3f464c783f%3A0x4661c60a0c6b37ca!2sFortaleza%20-%20CE!3m2!1d-3.7327203!2d-38.5270134!5e0!3m2!1spt-BR!2sbr!4v1622936737122!5m2!1spt-BR!2sbr" width="100%" height="600" style="border:0;" allowfullscreen="" loading="lazy"></iframe>'],
                            8:['Fortaleza', 'Fortaleza', 'https://pt.wikipedia.org/wiki/Fortaleza', '<iframe src="https://www.google.com/maps/embed?pb=!1m28!1m12!1m3!1d4062655.0742387506!2d-39.9173603306936!3d-6.071710740603618!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!4m13!3e6!4m5!1s0x7a9cf0cbdd3742b%3A0xe3e669d2b79586db!2sBelo%20Jardim%20-%20PE!3m2!1d-8.3872503!2d-36.4592707!4m5!1s0x7c74c3f464c783f%3A0x4661c60a0c6b37ca!2sFortaleza%20-%20CE!3m2!1d-3.7327203!2d-38.5270134!5e0!3m2!1spt-BR!2sbr!4v1622936824635!5m2!1spt-BR!2sbr" width="100%" height="600" style="border:0;" allowfullscreen="" loading="lazy"></iframe>'],
                            9:['Caririaçu', 'Caririacu', 'https://pt.wikipedia.org/wiki/Caririaçu', '<iframe src="https://www.google.com/maps/embed?pb=!1m28!1m12!1m3!1d2033779.8423875463!2d-39.98647123528331!3d-5.382439958150999!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!4m13!3e6!4m5!1s0x7a3d2f94027c6f1%3A0x2ea3064c989575d2!2zQ2FyaXJpYcOndSwgQ0U!3m2!1d-7.0417977!2d-39.2855054!4m5!1s0x7c74c3f464c783f%3A0x4661c60a0c6b37ca!2sFortaleza%20-%20CE!3m2!1d-3.7327203!2d-38.5270134!5e0!3m2!1spt-BR!2sbr!4v1622936768386!5m2!1spt-BR!2sbr" width="100%" height="600" style="border:0;" allowfullscreen="" loading="lazy"></iframe>'],
                            10:['General Sampaio', 'General Sampaio', 'https://pt.wikipedia.org/wiki/General_Sampaio', '<iframe src="https://www.google.com/maps/embed?pb=!1m28!1m12!1m3!1d509486.0833047714!2d-39.27152896765464!3d-3.945965822806705!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!4m13!3e6!4m5!1s0x7bf9ad2190e7101%3A0xdb8a6f8f415c8920!2sGeneral%20Sampaio%2C%20CE!3m2!1d-4.0438884!2d-39.454310199999995!4m5!1s0x7c74c3f464c783f%3A0x4661c60a0c6b37ca!2sFortaleza%20-%20CE!3m2!1d-3.7327203!2d-38.5270134!5e0!3m2!1spt-BR!2sbr!4v1622936792410!5m2!1spt-BR!2sbr" width="100%" height="600" style="border:0;" allowfullscreen="" loading="lazy"></iframe>']
                        }

        for i in dict_cidades:
            cidade_titulo = dict_cidades[i][0]
            cidade_html = dict_cidades[i][1]
            link = dict_cidades[i][2]
            self.mapa = dict_cidades[i][3]

            print('\n-------------------------------------')

            print('iniciando scrapping ...')
            self.scrapping(link)
            self.info_geral(cidade_html)

            print('carregando tamplate ...')
            self.substituir(cidade_titulo.upper())

            print('salvando novo site ...')
            self.salvar(cidade_html.title().replace(' ', '_'))

            print(f'\n ---> CIDADE: {cidade_titulo} OK!<--- ')

    def historia(self, cidade):
        html = requests.get(f"https://cidades.ibge.gov.br/brasil/ce/{cidade}/historico").content
        soup = BeautifulSoup(html, 'html.parser')

        print(f"https://cidades.ibge.gov.br/brasil/ce/{cidade}/historico")

        hist_titulo = soup.findAll("h2", attrs={"class":"hist__titulo"})
        historia_texto = soup.findAll("div", attrs={"class":"hist__texto"})

        rows = ''

        for i in historia_texto:
            rows += i.prettify()

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
