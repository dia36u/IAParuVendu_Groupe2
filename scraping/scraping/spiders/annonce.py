import scrapy

## remove unicode (\n\t...) from json

##info suppl:
# presence image 
# vendeur pro ou non
#
def normalize_whitespace(str):
            import re
            str = str.strip()
            str = re.sub(r'\s+', ' ', str)
            return str
class AnnoncesSpider(scrapy.Spider):
    name = "Annonces"  
    start_urls = [
    'https://www.paruvendu.fr/a/voiture-occasion/renault/scenic-ii/1260682580A1KVVORESC2',
    'https://www.paruvendu.fr/a/voiture-occasion/bmw/serie-3/1259702633A1KVVOBMS3',
    'https://www.paruvendu.fr/a/voiture-occasion/volkswagen/tiguan/1260770746A1KVVOVWTIG',
    'https://www.paruvendu.fr/a/voiture-occasion/bmw/serie-3/1258356486A1KVVOBMS3',
    'https://www.paruvendu.fr/a/voiture-occasion/bmw/serie-3/1260435637A1KVVOBMS3'
    ]

    

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

        next_page = response.css("a.linkToFT").attrib["href"]
        if next_page is not None:
            next_page="https://www.paruvendu.fr"+next_page
            yield scrapy.Request(next_page, callback=self.parse_page2, meta={'item': car_infos})

    def parse_page2(self, response):
        car_infos = response.meta['item']
        car_infos['prix commercialisation'] = normalize_whitespace(response.css("div#auto_pv_ongOn0TAB span::text")[-1].extract())

        next_page = response.css("div.cotea16-linkslist a").attrib["href"]
        if next_page is not None:
            next_page="https://www.paruvendu.fr"+next_page
            yield scrapy.Request(next_page, callback=self.parse_page3, meta={'item': car_infos})

    def parse_page3(self, response):
        
        car_infos = response.meta['item']
        car_infos['cote'] = normalize_whitespace(response.css("strong.ft_price::text").get())
        yield car_infos


    