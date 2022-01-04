# import the necessary packages
import scrapy
import pandas as pd
from datetime import datetime

# create a class with name of the Spider and inherit scrapy.Spider
class StockIpoQuotes(scrapy.Spider):
    # specify the name of the spider, this is used to run the code
    name = "ipo_quotes"
    # url to scrape
    start_urls = [
                    'https://www.moneycontrol.com/ipo/ipo-historic-table',
                 ]

    def parse(self, response):
        # save the scraped page as html file
        filename_html = 'ipo_quotes.html'
        with open(filename_html, 'wb') as h:
            h.write(response.body)
        # use xpath/css selector elements and inspect the corresponding page to scrape by id of the elements
        table = response.xpath('//*[@id="mytable"]')
        i=0
        # drill down to table elements
        row = table.xpath('//tr')
        # extract the text og the rows
        raw_data = row.xpath('td//text()').extract()
        # split the list sequentially
        idx = [i for i, v in enumerate(raw_data) if len(str(v)) == 8 and '-' in v]
        result = [raw_data[i:j] for i, j in zip(idx, idx[1:])]
        
        # scrap the column names
        head = table.xpath('//thead')
        
        cols = [i for i in head.xpath('tr//text()').extract() if '\r\n\t' not in i and '\xa0' not in i]
        # store in a dataframe
        ipo_data = pd.DataFrame(result)
        ipo_data.columns = cols[3:]
        ipo_data.to_csv('ipo_data.csv', index=False)

        yield {ipo_data.to_dict('list)}
