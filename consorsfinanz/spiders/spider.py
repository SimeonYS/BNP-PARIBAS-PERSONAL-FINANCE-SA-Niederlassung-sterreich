import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import ConsorsfinanzItem
from itemloaders.processors import TakeFirst
pattern = r'(\xa0)?'

class ConsorsfinanzSpider(scrapy.Spider):
	name = 'consorsfinanz'
	start_urls = ['https://www.consorsfinanz.at/presse-news/?L=0']

	def parse(self, response):

		posts = response.xpath('//div[@class="ce-textpic ce-center ce-below"]')
		items = []
		for post in posts:

			title = post.xpath('.//div[@class="ce-bodytext"]/h2/text()').get()
			content = post.xpath('.//div[@class="ce-textpic ce-center ce-below"]//p//text()').getall()[1:]
			content = [p.strip() for p in content if content.strip()]
			content = re.sub(pattern, "",' '.join(content))
			date = post.xpath('.//div[@class="ce-bodytext"]/p[1]/text()').get()

			item = ItemLoader(item=ConsorsfinanzItem(), response=response)
			item.default_output_processor = TakeFirst()

			item.add_value('title', title)
			item.add_value('link', response.url)
			item.add_value('content', content)
			item.add_value('date', date)
			items.append(item.load_item())
			return items
