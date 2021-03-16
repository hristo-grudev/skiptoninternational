import scrapy

from scrapy.loader import ItemLoader

from ..items import SkiptoninternationalItem
from itemloaders.processors import TakeFirst


class SkiptoninternationalSpider(scrapy.Spider):
	name = 'skiptoninternational'
	start_urls = ['https://www.skiptoninternational.com/news']

	def parse(self, response):
		post_links = response.xpath('//h2/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//li[@class="pager-next"]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="article-inner"]/div[@class="body generic-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="article-inner"]/div[@class="date"]/text()').get()

		item = ItemLoader(item=SkiptoninternationalItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
