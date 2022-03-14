import scrapy
from ..items import ParuVenduItem

class ParuVenduSpider(scrapy.Spider):
    name = "paru_vendu"
    start_urls = [
        'https://www.paruvendu.fr/a/voiture-occasion/audi/a3/'
    ]

    def parse(self, response):
        items = ParuVenduItem()
        nom_voiture = response.css('h3::text').extract()
        prix_vendeur = response.css('div class=ergov3-priceannonce-auto::text').extract()
        items['product_name'] = nom_voiture
        items['product_price'] = prix_vendeur
        yield items


