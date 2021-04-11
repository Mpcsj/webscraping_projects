# -*- coding: utf-8 -*-
import scrapy


class CountriesDebtSpider(scrapy.Spider):
    name = 'countries_debt'
    allowed_domains = [
        'worldpopulationreview.com/countries/countries-by-national-debt']
    start_urls = [
        'http://worldpopulationreview.com/countries/countries-by-national-debt/']

    def parse(self, response):
        table_content = response.xpath(
            "//table[@class='jsx-1487038798 table table-striped tp-table-body']/tbody/tr")
        for el in table_content:
            # print(f'row:{el}')
            yield{
                'country_name': el.xpath('.//td[1]/a/text()').get(),
                'gdp_debt': el.xpath('.//td[2]/text()').get(),
                'population': el.xpath('.//td[3]/text()').get()
            }
