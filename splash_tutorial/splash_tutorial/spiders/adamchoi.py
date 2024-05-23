import scrapy
from scrapy_splash import SplashRequest
from scrapy.http import HtmlResponse
class AdamchoiSpider(scrapy.Spider):
    name = 'adamchoi'
    allowed_domains = ['www.adamchoi.co.uk','localhost']
    # start_urls = ['http://www.adamchoi.co.uk/']

    # Copy and paste the lua code written in splash inside the script variable
    script = '''
        function main(splash, args)
          splash.private_mode_enabled = false
          assert(splash:go(args.url))
          assert(splash:wait(3))
          all_matches = assert(splash:select_all("label.btn.btn-sm.btn-primary"))
          all_matches[2]:mouse_click()
          assert(splash:wait(3))
          splash:set_viewport_full()
           return {
            html = splash:html(),
            png = splash:png(),
          }
        end
    '''

    # Define a start_requests function to connect scrapy and splash
    def start_requests(self):
        yield SplashRequest(url='https://www.adamchoi.co.uk/overs/detailed', callback=self.parse,
                            endpoint='execute', args={'lua_source':self.script})

    
    def parse(self, response):
        # Extract HTML content from JSON response
        html_content = response.data['html']

        # Create a new HtmlResponse object
        html_response = HtmlResponse(
            url=response.url,
            body=html_content,
            encoding='utf-8'
        )

        # Parse the new HtmlResponse object using XPath
        rows = html_response.xpath('//tr')

        for row in rows:
            date = row.xpath('./td[1]/text()').get()
            home_team = row.xpath('./td[2]/text()').get()
            score = row.xpath('./td[3]/text()').get()
            away_team = row.xpath('./td[4]/text()').get()
            yield {
                'date': date,
                'home_team': home_team,
                'score': score,
                'away_team': away_team,
            }