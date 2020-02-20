# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse
from scrapy.loader import ItemLoader

from firstSpider.items import greatGirlItem, GirlItemLoader
from firstSpider.util.commd import get_md5

class GreatgirlSpider(scrapy.Spider):
    name = 'greatGirl'
    allowed_domains = ['https://www.meitulu.com/']
    start_urls = ['https://www.meitulu.com/']

    def parse_detail(self, response):
        girl_item = greatGirlItem()
        head_img_url = response.meta.get("head_img_url", "")
        title = response.xpath("//div[@class='weizhi']/h1/text()").extract()
        num = response.xpath("//div[@class='c_l']/p/text()").extract()
        p_num = [element for element in num if element.strip().endswith("张")][0]
        match_re = re.match(r".*?(\d+).*?", p_num)
        if match_re:
            photoNum = int(match_re.group(1))
        else:
            photoNum = 0
        girl_item["head_image_url"] = [head_img_url]
        girl_item["title"] = title
        girl_item["photoNum"] = photoNum
        girl_item["url_object_id"] = get_md5(response.url)

        # 使用itemLoader处理网页
        itemLoader = GirlItemLoader(item=greatGirlItem(), response=response)
        itemLoader.add_xpath("title", "//div[@class='weizhi']/h1/text()")
        itemLoader.add_xpath("photoNum", "//div[@class='c_l']/p/text()")
        itemLoader.add_value("head_image_url", [head_img_url])
        itemLoader.add_value("url_object_id", get_md5(response.url))
        girl_loader = itemLoader.load_item()

        yield girl_item

    def parse(self, response):
        post_nodes = response.css("div.boxs li>a")
        for post_node in post_nodes:
            head_img_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"head_img_url": head_img_url},
                          callback=self.parse_detail, dont_filter=True)
