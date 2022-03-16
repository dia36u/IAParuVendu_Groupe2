import scrapy

# Récupère les URL à partir du fichier .txt
def splitURL(txt):
    my_file = open(txt, "r")
    content = my_file.read()
    url = content.splitlines()
    return url

# normalize_whitespace permet de supprimer les espaces, tabulations et sauts de ligne sur les données récoltées
# Utilisation de la biblio regex
def normalize_whitespace(str):
            import re
            # n'applique pas de mise en forme si les données sont null
            if str == None : return
            str = str.strip()
            # \s permet de match "\t\n\r\f\v"
            str = re.sub(r'\s+', ' ', str)
            return str        
class AnnoncesSpider(scrapy.Spider):
    name = "Annonces"  

    # start_urls va acueillir à terme, la liste de toutes les pages au sein desquelles nous allons récupérer
    # les annonces de voiture en vente sur le site ParuVendu
    
    # start_urls = splitURL(r"urls.txt")

    start_urls = [
        'https://www.paruvendu.fr/a/voiture-occasion/audi/q5/1260804894A1KVVOAUQ5',
        'https://www.paruvendu.fr/a/voiture-occasion/audi/a5/1260800372A1KVVOAUA5',
        'https://www.paruvendu.fr/a/voiture-occasion/audi/a6/1251779290A1KVVOAUA6',
        'https://www.paruvendu.fr/a/voiture-occasion/citroen/2-cv-dyane/1245883097A1KVVOCI2CV',
        'https://www.paruvendu.fr/a/voiture-occasion/citroen/c3/1260769359A1KVVOCIC3'
    ]

    # parse_page1 va permettre de récupérer la première vague d'information sur l'annonce du véhicule
    # Ces infos seront stockées dans le dictionnaire car_infos
    # La fonction va ensuite envoyer car_infos vers la fonction parse_page2
    
    def parse(self, response):
        information=response.css('div.cotea16-graphic')
        car_infos = {
            'version': normalize_whitespace(information.css("li.vers span ::text").get()),
            'prix': normalize_whitespace(information.css("li.px span ::text").get()),
            'annee': normalize_whitespace(information.css("li.ann span ::text").get()),
            'kilometrage': normalize_whitespace(information.css("li.kil span ::text").get()),
            'energie': normalize_whitespace(information.css("li.en span ::text").get()),
            'emission co2': normalize_whitespace(information.css("li.emiss span ::text").get()),
            'consommation mixte': normalize_whitespace(information.css("li.cons span ::text").get()),
            'transmission': normalize_whitespace(information.css("li.vit span ::text").get()),
            'nombre de porte': normalize_whitespace(information.css("li.carro span ::text").get()),
            'puissance fiscale': normalize_whitespace(information.css("li.puiss span ::text").get()),
            'nombre de places': normalize_whitespace(information.css("li.por span ::text").get()),
            'couleur': normalize_whitespace(information.css("li.nologo span::text").get())
        }

        # Récupération du lien vers la fiche technique du véhicule
        next_page = response.css("a.linkToFT").attrib["href"]
        if next_page is not None:
            next_page="https://www.paruvendu.fr"+next_page
            yield scrapy.Request(next_page, callback=self.parse_page2, meta={'item': car_infos})

    # parse_page2 va permettre de récupérer l'info du prix de commercialisation
    # Cette info est ajoutée à car_infos puis envoyée vers parse_page3

    def parse_page2(self, response):
        car_infos = response.meta['item']
        car_infos['prix commercialisation'] = normalize_whitespace(response.css("div#auto_pv_ongOn0TAB span::text")[-1].extract())

        # Récupération du lien vers la fiche de cotation du véhicule
        next_page = response.css("div.cotea16-linkslist a").attrib["href"]
        if next_page is not None:
            next_page="https://www.paruvendu.fr"+next_page
            yield scrapy.Request(next_page, callback=self.parse_page3, meta={'item': car_infos})

    # parse_page3 va permettre de récupérer la cote du véhicule
    # Cette info est ajoutée à car_infos

    def parse_page3(self, response):
        
        car_infos = response.meta['item']
        car_infos['cote'] = normalize_whitespace(response.css("strong.ft_price::text").get())
        yield car_infos
