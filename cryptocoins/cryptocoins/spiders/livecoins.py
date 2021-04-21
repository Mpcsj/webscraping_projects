# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

class LivecoinsSpider(scrapy.Spider):
    name = 'livecoins'
    allowed_domains = ['www.web.archive.org/web/20200116052415/https://www.livecoin.net/en/']
    # start_urls = ['https://web.archive.org/web/20200116052415/https://www.livecoin.net/en//']
    lua_script = '''
        function main(splash, args)
            splash.private_mode_enabled = false
            url = args.url
            assert(splash:go(url))
            assert(splash:wait(5))
            rur_tab = assert(splash:select_all(".filterPanelItem___2z5Gb"))
            rur_tab[5]:mouse_click()
            assert(splash:wait(1))
            splash:set_viewport_full()
            return splash:html()
        end
    '''

    def start_requests(self):
        yield SplashRequest(url="https://web.archive.org/web/20200116052415/https://www.livecoin.net/en/", callback=self.parse, endpoint="execute", args={
            'lua_source': self.lua_script
        })

    def parse(self, response):
        print(f'{20*"*"}chegou em parse:{20*"*"}')
        # print(response.body)
        # yield {
        #     'content':response.body
        # }
        for currency in response.xpath("//div[contains(@class, 'ReactVirtualized__Table__row tableRow___3EtiS')]"):
            print('atual:',currency)
            yield{
                'currency pair': currency.xpath(".//div[1]/div/text()").get(),
                'volume(24h)': currency.xpath(".//div[2]/span/text()").get()
            }