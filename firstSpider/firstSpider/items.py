# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import re

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
from scrapy.loader import ItemLoader


def selectPhotoNum(values):
    if values.strip().endswith("张"):
        match_re = re.match(r".*?(\d+).*?", values)
        if match_re:
            photoNum = int(match_re.group(1))
        else:
            photoNum = 0
        return photoNum


class FirstspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class GirlItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class greatGirlItem(scrapy.Item):
    head_image_url = scrapy.Field()
    title = scrapy.Field()
    photoNum = scrapy.Field(
        input_processor=MapCompose(selectPhotoNum)
    )
    head_image_path = scrapy.Field()
    url_object_id = scrapy.Field()
    pass
