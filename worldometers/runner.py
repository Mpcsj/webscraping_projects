# com este arquivo, eu consigo executar um crawler programaticamente
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from worldometers.spiders.countries_data import CountriesDataSpider

process = CrawlerProcess(settings=get_project_settings())
process.crawl(CountriesDataSpider)
process.start()