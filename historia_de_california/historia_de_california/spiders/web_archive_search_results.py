# this spider outputs the result urls of a filtered 'banc mss' search


import scrapy


archive_org = 'https://archive.org'
urls = [
       f'{archive_org}/search.php?query=banc+mss&and%5B%5D=collection%3A%22bancroft_library%22&and%5B%5D=collection%3A%22microfilm%22&and%5B%5D=collection%3A%22fav-hija_de_grijalva%22&and%5B%5D=collection%3A%22americana%22&and%5B%5D=creator%3A%22vallejo%2C+mariano+guadalupe%2C+1808-1890%22&and%5B%5D=creator%3A%22savage%2C+thomas%2C+b.+1823%22&and%5B%5D=creator%3A%22savage%2C+thomas%2C+b.+1823.+trc%22&page={page}' 
       for page in range(1, 3+1)
       ]  # in this case there are 3 pages of results; num_of_results / 50 = num_of_pages


class WebArchiveSearchResultsSpider(scrapy.Spider):
    name = 'web_archive_search_results'
    start_urls = urls

    def parse(self, response):
        for short_url in response.xpath('//*[@class="results"]//@href').getall():
            if '/details/bancroft_library' not in short_url:
                yield {
                        'result_url': archive_org + short_url
                }

