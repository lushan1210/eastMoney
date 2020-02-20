# -*- coding: utf-8 -*-
import scrapy
import json
import base64
from io import BytesIO
from PIL import Image
from firstSpider.util.commd import base64_captcha

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    captcha_url = "https://www.zhihu.com/api/v3/oauth/captcha?lang=en"
    header = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en',
    }

    def parse(self, response):
        pass

    def start_requests(self):
        return [scrapy.Request(url='https://www.zhihu.com/signin?next=%2F', callback=self.login, headers=self.header)]

    def login(self, response):
        yield scrapy.Request(url=self.captcha_url, callback=self.parse_get_captcha, headers=self.header)

    def parse_get_captcha(self, response):
        is_captcha = json.loads(response.text) .get("show_captcha")
        secondCaptchaCookie = self.header
        secondCaptchaCookie['Set-Cookie'] = response.headers.getlist('Set-Cookie')
        if is_captcha:
            yield scrapy.Request(url=self.captcha_url, method='PUT', callback=self.parse_image_url, headers=secondCaptchaCookie)

    def parse_image_url(self, response):
        img_url = json.loads(response.text).get('img_base64')
        img_data = base64.b64decode(img_url)
        img_real = BytesIO(img_data)
        img = Image.open(img_real)
        img.save('captcha.png')
        captcha_str = base64_captcha(img_url)
        yield scrapy.FormRequest(
            url=self.captcha_url,
            callback=self.parse_post_captcha,
            formdata={
                'input_text': str(captcha_str)
            },
            headers=self.header
        )
        return ""

    def parse_post_captcha(self, response):
        result = json.loads(response.text).get("success", '')
        if result:
            print("验证码正确")
        return ""