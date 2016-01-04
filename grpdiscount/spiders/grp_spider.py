import scrapy
import json
from grpdiscount.items import GrpItem
import xlwt
import xlrd


class grp_spider(scrapy.Spider):
    name = "discount"
    allowed_domains = ['housing.com']
    start_urls = [
        "https://housing.com/in/buy/search?f=eyJsb2N0IjoicG9seSIsInBhZ2VfbnVtIjozLCJwb2x5Ijp7ImlkIjoiNTdkNjM4MTJjZjg5OWJiOWI3ZDIiLCJidWZmZXIiOmZhbHNlfSwibnBfdG90YWxfY291bnQiOjQxMywicmVzYWxlX3RvdGFsX2NvdW50IjoxMDkwMCwibnBfb2Zmc2V0IjotMiwicmVzYWxlX29mZnNldCI6MH0%3D"
    ]

    def add_in_sheet(self,item):
        workbook = xlwt.Workbook()
        #workbook.save('grpdiscount.xls')
        sheet = workbook.add_sheet('Sheet_1')
        sheet.write(0,0,'Project Url')
        sheet.write(0,1,item['project_url'])
        sheet.write(1,0,'Name')
        sheet.write(1,1,item['property_name'])
        sheet.write(2,0,'Address')
        sheet.write(2,1,item['address'])
        sheet.write(3,0,'Status')
        sheet.write(3,1,"")
        sheet.write(4,0,'Email')
        sheet.write(4,1,"")
        sheet.write(5,0,'Phone')
        sheet.write(5,1,"")
        sheet.write(7,0,'price_per_sqft')
        sheet.write(7,1,item['price_per_sqft'])
        sheet.write(8,0,'Total Project Area')
        sheet.write(8,1,item['total_area'])
        sheet.write(9,0,'Launch Date')
        sheet.write(9,1,"")
        sheet.write(10,0,'Possession Date')
        sheet.write(10,1,item['possession_date'])
        sheet.write(11,0,'Type')
        col = 1
        for bhk in item['property_bhk']:
            sheet.write(11,col,bhk)
            col+=1
        sheet.write(12,0,'Bedrooms')
        sheet.write(12,1,"")
        sheet.write(13,0,'Bathrooms')
        sheet.write(13,1,'')
        sheet.write(14,0,'Area Sq. Ft.')
        prop = item['property_size']
        for i in range(len(prop)):
            sheet.write(14,i+1,prop[i])
        sheet.write(6,0,'Area-range')
        min_area = prop[0]
        max_area = prop[-1]
        sheet.write(6,1,min_area + '-' + max_area)
        sheet.write(15, 0,'Price')
        prop = item['property_price']
        for i in range(len(prop)):
            sheet.write(15,i+1,prop[i])
        sheet.write(16,0,'Carpet Area')
        sheet.write(16,1,'')
        sheet.write(17,0,'Facing')
        sheet.write(17,1,'')
        sheet.write(18,0,'Description')
        sheet.write(18,1,'Description of Project')
        sheet.write(19,1,item['description'])
        sheet.write(20,0,'Speciality')
        sheet.write(20,1,item['speciality'])
        sheet.write(21,0,'About Builder')
        sheet.write(21,1,item['builder_desc'])
        sheet.write(22,0,'Certifications')
        sheet.write(22,1,'')
        sheet.write(23,0,'unit')
        sheet.write(23,1,item['total_apartment'])
        sheet.write(24,0,'Videos')
        col = 1
        temp = item['photos']
        if temp:
            for video in temp:
                if 'youtube' in video:
                    sheet.write(24,col,video)
                    col += 1
        sheet.write(25,0,'Amenities')
        sheet.write(25,1,item['amenities'])
        sheet.write(26,0,'Main Image')
        sheet.write(26,1,item['main_image'])
        sheet.write(27,0,'galary Image')
        col =1
        temp = item['photos']
        for image in temp:
            if not 'youtube' in image:
                sheet.write(27,col,image)
                col+=1
        workbook.save(item['property_name']+'.xlsx')


    def parse_dir_contents(self, response):
        item = GrpItem()
        temp = format(response.xpath('//div[@class="image"]/div[@class="img"]/@style').extract())
        if temp:
            temp = temp[3:-2]
            temp = temp.strip('background-image:url')
            item['main_image'] = temp
        temp = format(response.xpath("//h1[@class='main-text']/text()").extract())
        item['property_name'] = temp[3:-2]
        temp = format(response.xpath('//div[@class="location-info"]/text()').extract())
        item['address'] = temp[3:-2] 
        temp = format(response.xpath('//div[@class="builder-text"]/text()').extract())
        item['builder_name'] = temp[6:-2]
        item['total_apartment']=''
        item['total_area'] = ''
        item['possession_date'] = ''
        for entity in response.xpath('//section[@class="basic"]/span[@class = "entity"]'):
            temp = entity.xpath('span[@class="entity-right"]/span[@class="text"]/text()').extract()
            temp = format(temp)
            temp = temp[3:-2]
            if temp == 'Project Size':
                temp = entity.xpath('span[@class="entity-right"]/span[@class="value"]/span[last()]/text()').extract()
                temp = format(temp)
                temp = temp[3:-2]
                item['total_apartment'] = temp
            elif temp == 'Project Area' :
                temp = entity.xpath('span[@class="entity-right"]/span[@class="value"]/span[1]/text()').extract()
                temp = format(temp)
                temp = temp[3:-2]
                item['total_area'] = temp
                temp = format(entity.xpath('span[@class="entity-right"]/span[@class="value"]/span[2]/text()').extract())
                if temp :
                    temp = temp[3:-2]
                    item['total_area'] += temp
            elif temp == 'Possession Starts' or temp == "Possession":
                temp = entity.xpath('span[@class="entity-right"]/span[@class="value"]/span/text()').extract()
                temp = format(temp)
                temp = temp[3:-2]
                item['possession_date'] = temp
        temp = format(response.xpath('//p[@class="desc-para"]/text()').extract())
        item['description'] = temp[3:-2]
        title = format(response.xpath('//section[@class="utilities"]/h3/text()').extract())
        if title == "[u'Project Amenities']":
	        temp = format(response.xpath('//span[@class="amenity-entity"]/span[@class="text"]/text()').extract())
	        if temp:
		        temp = temp.replace("u'",'')
		        temp = temp.replace('u"','')
		        temp = temp.replace("'",'')
		        temp = temp[1:-1]
		        temp = temp.replace(',','\n')
		        item['amenities'] = temp
		
        buil = format(response.xpath('//div[@class="builder-desc"]/div[@class="title"]/text()').extract())
        if buil[3:-2]  == item['builder_name'] :
        	temp = format(response.xpath('//div[@class="builder-desc"]/span[@class="builder-desc-para"]/p/text()').extract())
        	item['builder_desc'] = temp[3:-2]
        	temp = format(response.xpath('//div[@class="builder-details inb-vt"]/div[@class="established"]/div[@class="value"]/text()').extract())
        	item['builder_desc'] += '\n'
        	item['builder_desc'] += 'Establised in: ' + temp[3:-2] + '\n' + 'Total Project: '
        	temp = format(response.xpath('//div[@class="builder-details inb-vt"]/div[@class="total-projects"]/div[@class="value"]/text()').extract())
        	item['builder_desc'] += temp[3:-2]
        item['speciality']  = ''
        for inte in response.xpath('//div[@class="interior-body"]/div[@class="interior-card"]'):
        	t1 = format(inte.xpath('div[@class="header-text-secondary"]/text()').extract())
        	item['speciality'] += t1[3:-2] + '\n'
        	for pills in inte.xpath('div[@class="pills"]'):
        		inte_head = format(pills.xpath('span[@class="header"]/text()').extract())
        		inte_head = inte_head[3:-2]
        		inte_body = format(pills.xpath('span[@class="texts"]/text()').extract())
        		inte_body = inte_body[3:-2] 
        		pill = inte_head+inte_body + '\n'
        		item['speciality'] += pill
        temp = format(response.xpath('//div[@class="list-heading"]/span[@class="area"]/text()').extract())
        if temp:
	        temp = temp.replace("u'",'')
	        temp = temp.replace('u"','')
	        temp = temp.replace("'",'')
	        temp = temp[1:-1]
	        temp = temp.split(',')
	        item['property_size'] = temp

		temp = format(response.xpath('//div[@class="list-price"]/span[@class="price-text"]/text()').extract())
        if temp:
	        temp = temp.replace("u'",'')
	        temp = temp.replace('u"','')
	        temp = temp.replace("'",'')
	        temp = temp[1:-1]
	        temp = temp.split(',')
	        item['property_price'] = temp
        temp = format(response.xpath('//div[@data-type="photos"]/img/@src').extract())
        item['photos'] = []
        if temp:
            temp = temp.replace("u'",'')
            temp = temp.replace('u"','')
            temp = temp.replace("'",'')
            temp = temp[1:-1]
            temp = temp.split(',')
            for i in range(len(temp)) :
                if 'youtube' in temp[i]:
                    t = temp[i]
                    youtube = "https://www.youtube.com/watch?v=" + t[27:38]
                    temp[i] = youtube
            item['photos'] = temp
        temp = format(response.xpath('//div[@class="hide-embed rate"]/text()').extract())
        item['price_per_sqft'] = temp[3:-4]
        temp = format(response)
        item['project_url'] = temp[5:-1]
        item['property_bhk']=[]
        for header in response.xpath('//div[@class="nsv-list-item-container"]/div/span[@class="header-text"]'):
            t1 = format(header.xpath('span[@class="header-text-config"]/text()').extract())
            t1 = t1[3:-2]
            t2 = format(header.xpath('span[@class="header-text-type"]/span[last()]/text()').extract())
            t2 = int(t2[4:-3])
            for i in range(t2):
                item['property_bhk'] += [t1]

        self.add_in_sheet(item)


    def parse(self, response):
        count = 0
        for href in response.xpath('//div[@class="results-container"]/div[@class="list-card-item"]/div[@data-type="projects"]/div[@class="list-details"]/a[@class="list-name"]/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)



