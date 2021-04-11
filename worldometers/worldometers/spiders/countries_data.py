# -*- coding: utf-8 -*-
import scrapy
import logging
TAG = 'countries_data'


class CountriesDataSpider(scrapy.Spider):
    name = 'countries_data'
    allowed_domains = ['www.worldometers.info']
    start_urls = [
        'https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        countries = response.xpath('//td/a')  # busco a partir da raiz
        for country in countries:
            # print(f'curr country:{country}')
            # começo com "." pois é um caminho relativo ao subelemento atual
            name = country.xpath('.//text()').get()
            link = country.xpath('.//@href').get()
            print('Dados obtidos, url:{}'.format(link))
            print(f'country_name:{name}::url:{link}')
            # follow_link = f'https://www.worldometers.info{link}' # forma 1 de fazer
            # follow_link = response.urljoin(link) # forma 2 de fazer
            # yield scrapy.Request(url=follow_link)
            # forma 3 de fazer
            yield response.follow(
                url=link,
                callback=self.parse_country_content,
                meta={
                    'country_name': name
                }
            )
            # obs: o atributo meta permite a passagem de conteúdo entre funções
            # como no caso aqui, que foi usado com a funcao de callback

    def parse_country_content(self, response):
        logging.info(response.url)
        rows = response.xpath(
            "(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr")
        curr_data = []
        for row in rows:
            year = row.xpath('.//td[1]/text()').get()
            population = row.xpath('.//td[2]/strong/text()').get()

            curr_data.append({
                'year': year,
                'population': population
            })
        yield {
            'country': response.request.meta['country_name'],
            'content': curr_data
        }
