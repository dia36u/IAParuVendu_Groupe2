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
    'https://www.paruvendu.fr/a/voiture-occasion/volkswagen/tiguan/1260770746A1KVVOVWTIG'
    ]

    def parse(self, response):
        for information in response.css('div.cotea16-graphic'):
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
                'couleur': information.css("li.nologo span::text").get()
            }
        next_page = response.css("a.linkToFT").attrib["href"]
        if next_page is not None:
            next_page="https://www.paruvendu.fr"+next_page
            yield scrapy.Request(next_page, callback=self.parse_page2)

    def parse_page2(self, response):
        yield {
            "prix commercialisation" : response.css("div#auto_pv_ongOn0TAB span::text")[-1].extract(),
         }

        next_page = response.css("div.cotea16-linkslist a").attrib["href"]
        if next_page is not None:
            next_page="https://www.paruvendu.fr"+next_page
            yield scrapy.Request(next_page, callback=self.parse_page3)

    def parse_page3(self, response):
        yield {
            "cote" : response.css("strong.ft_price::text").get()
         }


    