import scrapy

## remove unicode (\n\t...) from json

##info suppl:
# presence image 
# vendeur pro ou non
#

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
            'version': information.css("li.vers span ::text").get(),
            'prix': information.css("li.px span ::text").get().strip(),
            'annee': information.css("li.ann span ::text").get().strip(),
            'kilometrage': information.css("li.kil span ::text").get(),
            'energie': information.css("li.en span ::text").get().strip(),
            'emission co2': information.css("li.emiss span ::text").get(),
            'consommation mixte': information.css("li.cons span ::text").get(),
            'transmission': information.css("li.vit span ::text").get().strip(),
            'nombre de porte': information.css("li.carro span ::text").get().strip(),
            'puissance fiscale': information.css("li.puiss span ::text").get(),
            'nombre de places': information.css("li.por span ::text").get().strip(),
            'couleur': information.css("li.nologo span::text").get().strip()
        }

        next_page = response.css("a.linkToFT").attrib["href"]
        if next_page is not None:
            next_page="https://www.paruvendu.fr"+next_page
            yield scrapy.Request(next_page, callback=self.parse_page2, meta={'item': car_infos})

    def parse_page2(self, response):
        car_infos = response.meta['item']
        car_infos['prix commercialisation'] = response.css("div#auto_pv_ongOn0TAB span::text")[-1].extract().strip()

        next_page = response.css("div.cotea16-linkslist a").attrib["href"]
        if next_page is not None:
            next_page="https://www.paruvendu.fr"+next_page
            yield scrapy.Request(next_page, callback=self.parse_page3, meta={'item': car_infos})

    def parse_page3(self, response):
        car_infos = response.meta['item']
        car_infos['cote'] = response.css("strong.ft_price::text").get().strip()
        yield car_infos


    