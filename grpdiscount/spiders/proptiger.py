import scrapy
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.http import TextResponse
from grpdiscount.items import GrpItem
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
class SearchSpider(scrapy.Spider):
    name = "proptiger"

    allowed_domains = ['www.proptiger.com']
    start_urls = ['https://www.proptiger.com/noida/sector-118/supertech-romano-652425']

    def __init__(self, filename=None):
        # wire us up to selenium
        self.driver = webdriver.Firefox()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        self.driver.close()

    def parse(self, response):
        item = GrpItem()
        # Load the current page into Selenium
        self.driver.get(response.url)

        try:
            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, '//a[@class="btn-action"]')))
        except TimeoutException:
            print "Time out"
            return

        # Sync scrapy and selenium so they agree on the page we're looking at then let scrapy take over
        resp = TextResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8');

        temp = format(resp.xpath('//*[@id="views"]/div/div/div[2]/div/div[2]/div/div[1]/div/div/div[1]/div/h1/span/text()').extract())
        item['property_name'] = temp[3:-2]

        main_address = format(resp.xpath('//*[@id="views"]/div/div/div[2]/div/div[2]/div/div[1]/div/div/div[2]/div[1]/span/text()').extract())
        locality = format(resp.xpath('//*[@id="views"]/div/div/div[2]/div/div[2]/div/div[1]/div/div/div[2]/div[2]/span/text()').extract())
        item['address'] = main_address[3:-2] +  ', ' + locality[3:-2]
        builder_name = format(resp.xpath('//*[@id="views"]/div/div/div[3]/div/div[6]/div[5]/div/div[1]/div/div/span/text()').extract())
        builder_name = builder_name[3:-2]
        builder_name = builder_name.split()
        if len(builder_name) > 1:
            item['builder_name'] = builder_name[1]

        for entity in resp.xpath('//div[@id="overview"]/div/div[2]/div/span'):
            heading = format(entity.xpath('b/text()').extract()).lower()
            if heading[3:-2] == 'status':
                value = format(entity.xpath('text()').extract())
                item['status'] = value[3:-2]
            if heading[3:-2] == 'possession :' or heading[3:-2] == 'completed :':
                value = format(entity.xpath('text()').extract())
                item['possession_date'] = value[3:-2]
            if heading[3:-2] == 'sizes':
                value = format(entity.xpath('text()').extract())
                item['area_range'] = value[3:-2]
            if heading[3:-2] == 'total area':
                value = format(entity.xpath('text()').extract())
                item['total_area'] = value[3:-2]
            if heading[3:-2] == 'total apartments':
                value = format(entity.xpath('text()').extract())
                item['total_apartment'] = value[3:-2]
            if heading[3:-2] == 'launch date':
                value = format(entity.xpath('text()').extract())
                item['launch_date'] = value[3:-2]

        try :
            desc = self.driver.find_element_by_xpath('//*[@id="overview"]/div/div[3]/div/span[2]')
        except:
            print "Description not available"
        if desc:
            try:
                desc.click()
                WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="overview"]/div/div[3]/div/span[@data-ng-click="updateFlag(false)"]')))
                resp = TextResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8');
            except:
                print 'Full description is not available....'
        description = format(resp.xpath('//*[@id="overview"]/div/div[3]/div/span[@itemprop="description"]/text()').extract())
        item['description'] = description[3:-2]

        

        #yield item