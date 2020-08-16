# spider for scraping metadata


import scrapy


class ScrapeWebArchiveResultsSpider(scrapy.Spider):
    name = 'scrape_web_archive_results'

    def start_requests(self):
        with open('./web_archive_result_urls.txt') as url_list:
            urls_to_scrape = url_list.read().split('\n')
        for url in urls_to_scrape:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):

        document_name = response.xpath(
                '//*[@id="maincontent"]//*[@itemprop="name"]/text()'
        ).get()

        document_url = response.url

        description = response.xpath('//*[@id="descript"]/text()').getall()

        publication_date = response.xpath(
                '//*[@id="maincontent"]//dl[contains(., "Publication date")]//span/text()'
        ).get()

        collection_detail = []
        details = response.xpath('//*[@id="maincontent"]//div//dl//@href').getall()
        for d in details:
            if 'details' in d:
                collection_detail.append(d.split('/')[-1])

        sponsor = response.xpath(
                '//*[@id="maincontent"]//div//*[@class="metadata-definition"][contains(., "sponsor")]//a/text()'
        ).get()

        language = response.xpath(
                '//*[@id="maincontent"]//div//dl[contains(., "Language")]//a/text()'
        ).get()

        volume = response.xpath(
                '//*[@id="maincontent"]//div//dl[contains(., "Volume")]/dd/text()'
        ).get()

        call_number = response.xpath(
                '//*[@id="maincontent"]//*[@class="metadata-definition"][contains(., "Call number")]/dd/text()'
        ).get()

        collection_library = response.xpath(
                '//*[@id="maincontent"]//div//*[@class="metadata-definition"][contains(., "Collection-library")]/dd/text()'
        ).get()

        external_identifier = response.xpath(
                '//*[@id="maincontent"]//dl[contains(., "External-identifier")]//a/text()'
        ).get().strip(' \n')

        external_identifier_url = response.xpath(
                '//*[@id="maincontent"]//dl[contains(., "External-identifier")]//a/@href'
        ).get()

        identifier = response.xpath(
                '//*[@id="maincontent"]//dl[contains(., "Identifier")]//span/text()'
        ).get()

        identifier_ark = response.xpath(
                '//*[@id="maincontent"]//dl[contains(., "Identifier-ark")]//dd/text()'
        ).get()

        identifier_bib = response.xpath(
                '//*[@id="maincontent"]//dl[contains(., "Identifier-bib")]//dd/text()'
        ).get()

        pages = response.xpath(
                '//*[@id="maincontent"]//dl[contains(., "Pages")]//dd/text()'
        ).get()

        yield {
                'document_name': document_name,
                'document_url': document_url,
                'publication_date': publication_date,
                'description': description,
                'collection_detail': collection_detail,
                'sponsor': sponsor,
                'language': language,
                'volume': volume,
                'call_number': call_number,
                'collection_library': collection_library,
                'external_identifier': external_identifier,
                'external_identifier_url': external_identifier_url,
                'identifier': identifier,
                'identifier_ark': identifier_ark,
                'identifier_bib': identifier_bib,
                'pages': pages,
        }

