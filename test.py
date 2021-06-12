from bs4 import BeautifulSoup
import requests

cidade = 'fortaleza'

html = requests.get(f"https://cidades.ibge.gov.br/brasil/ce/tururu/historico").content
soup = BeautifulSoup(html, 'html.parser')

hist_titulo = soup.find("h2", attrs={"class": "hist__titulo"})
historia_texto = soup.findAll("div", attrs={"class": "hist__texto"})

print(soup.prettify())