from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from digikey_productlist.items import DigikeyProductlistItem

class MySpider(CrawlSpider):
    name = "digikeyproduct"
    allowed_domains = ["digikey.com"]
    start_urls = ["http://www.digikey.com/product-search/en?FV=fff40027%2Cfff800cd&mnonly=0&newproducts=0&ColumnSort=0&page=1&stock=0&pbfree=0&rohs=0&quantity=&ptm=0&fid=0&pageSize=500"]
    rules = (Rule (SgmlLinkExtractor(allow=("", ),restrict_xpaths=('//*[@id="content"]/div[8]/div/a[12]',)), callback="parse_items", follow= True),
    )

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        titles = hxs.select("//table[@class='stickyHeader']/tbody/tr")
        items = []
        for titles in titles:
            item = DigikeyProductlistItem()
            item ["Digikey_Part_Number"] = titles.select("td[@class='digikey-partnumber']/a/text()").extract()
            item ["Product_link"] = titles.select("td[@class='digikey-partnumber']/a/@href").extract()
            #item ["Digikey_Part_Number_Link"] = titles.select("td[@class='digikey-partnumber']/a/@href").extract()
            items.append(item)
        return items

#//*[@id="content"]/div[8]/div/a[12]
            #http://www.digikey.com/product-search/en/integrated-circuits-ics/embedded-microcontrollers/2556109/page/2
