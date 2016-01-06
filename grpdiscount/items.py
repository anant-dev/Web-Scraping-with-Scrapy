# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GrpItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    area_range = scrapy.Field()
    status = scrapy.Field()
    project_url = scrapy.Field()
    photos = scrapy.Field()
    property_name = scrapy.Field()
    builder_name = scrapy.Field()
    address = scrapy.Field()
    total_apartment = scrapy.Field()
    total_area = scrapy.Field()
    launch_date = scrapy.Field()
    possession_date = scrapy.Field()
    description = scrapy.Field()
    amenities = scrapy.Field()
    builder_desc = scrapy.Field()
    property_bhk = scrapy.Field()
    property_size = scrapy.Field()
    property_price = scrapy.Field()
    bedroom = scrapy.Field()
    bathroom = scrapy.Field()
    speciality = scrapy.Field()
    price_per_sqft = scrapy.Field()
    carpet_area = scrapy.Field()
    facing = scrapy.Field()
    certification = scrapy.Field()
    main_image = scrapy.Field()