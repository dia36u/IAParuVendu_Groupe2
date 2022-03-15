from re import M
import requests
from requests import get
from bs4 import BeautifulSoup
import json

marques=["Audi","Citroen","Dacia","Fiat","Ford","Mercedes","Nissan","Opel","Peugeot","Renault","Toyota","Volkswagen"]
listes_annonces = []

url="https://www.paruvendu.fr/a/voiture-occasion/"

marque_model={}
for marque in marques:
    page = requests.get(url+str(marque.lower()))
    if page.ok:

        soup = BeautifulSoup(page.content, 'html.parser')

        select= soup.find('select',{"id":"md"})

        options =select.find_all('option')
        model=[model.text for model in options[1:-1]]
        marque_model[marque]=model

with open('marque_model.json', 'w') as f:
    json.dump(marque_model, f)
    