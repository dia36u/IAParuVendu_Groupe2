import requests
from requests import get
from bs4 import BeautifulSoup
import json 
import unidecode

f=open("../../marque_model.json")
marques_modeles=json.load(f)
print(marques_modeles)
listes_annonces = []
for marque,modele in marques_modeles.items():

    url=f"https://www.paruvendu.fr/a/voiture-occasion/{marque}/"
    for each in modele:
        new_url=url+unidecode.unidecode(each)
        page = requests.get(new_url+"/?p="+"1")
        
        
        if page.ok:

            soup = BeautifulSoup(page.text, 'html.parser')
            if soup.find_all('div', class_='lazyload_bloc ergov3-annonce ergov3-annonceauto'):
                print('yes bro')
                if soup.find('a',{'class':'page'}):
                    print('and more')
            else:
                print('nope')
            # page = requests.get(url+"/?p="+str(i))
            # divs= soup.find_all('div', class_='lazyload_bloc ergov3-annonce ergov3-annonceauto')
            # for div in divs:
            #     listes_annonces.append(div.find('a').get("href"))



# with open("urls.txt", "w") as opfile:
#     opfile.write("\n".join(listes_annonces))


