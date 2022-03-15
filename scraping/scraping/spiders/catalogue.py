import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

from time import sleep
from random import randint

listes_annonces = []
url="https://www.paruvendu.fr/a/voiture-occasion/audi/?p="

for i in range(1,5):


    page = requests.get(url+str(i))

    soup = BeautifulSoup(page.text, 'html.parser')

    divs= soup.find_all('div', class_='lazyload_bloc ergov3-annonce ergov3-annonceauto')
    for div in divs:
        listes_annonces.append(div.find('a').get("href"))

print(len(listes_annonces))




