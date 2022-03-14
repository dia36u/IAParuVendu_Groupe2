import scrapy

class AnnoncesSpider(scrapy.Spider):
    name = "Annonces"  
    start_urls = [
    'https://www.paruvendu.fr/a/voiture-occasion/renault/scenic-ii/1260682580A1KVVORESC2',
    'https://www.paruvendu.fr/a/voiture-occasion/bmw/serie-3/1259702633A1KVVOBMS3'
    ]
    def parse(self, response):
         for information in response.css('div.cotea16-graphic ul').get[0]:
            yield {
                'version': information.css("li.vers span ::text").get(),
                'prix': information.css("li.px span ::text").get(),
                'annee': information.css("li.ann span ::text").get(),
                'kilometrage': information.css("li.kil span ::text").get(),
                'energie': information.css("li.en span ::text").get(),
                'emission co2': information.css("li.emiss span ::text").get(),
                'consommation mixte': information.css("li.cons span ::text").get(),
                'transmission': information.css("li.vit span ::text").get(),
                'nombre de porte': information.css("li.carro span ::text").get(),
                'puissance fiscale': information.css("li.puiss span ::text").get(),
                'nombre de places': information.css("li.por span ::text").get(),
            }

    