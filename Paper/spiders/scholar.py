from ast import Yield
from mimetypes import init
from subprocess import call
import scrapy
from pathlib import Path


class GGScholarSpider(scrapy.Spider):
    name = "ggscholar"
    index = 'https://scholar.google.com'
    paper_dir_parent = Path('./papers')

    start_page = 20
    page_size = 80
    specialChars = "\/:?\"<>|" 
    def __init__(self, author, **kwargs):
        self.author = author
        self.start_urls = [
        'https://scholar.google.com/citations?user=%s&hl=en&oi=ao' % author,
    ]
        super().__init__(**kwargs)

    def parse(self, response):
        author_name = response.css('#gsc_prf_in::text').get()
        self.paper_dir = Path(self.paper_dir_parent, author_name)
        load_more = 1 - ('disabled' in response.css('#gsc_bpf_more').extract())
        for title in response.css('tbody#gsc_a_b').css('tr.gsc_a_tr'):
            # if title.css('a.gsc_a_at::text').get() == None:
            #     return
            # if len(title.css('.gs_gray::text')) > 1:
            #     yield{
            #         'tiltle': title.css('a.gsc_a_at::text').get(),
            #         'authors': title.css('.gs_gray::text')[0].get(),
            #         'journal': title.css('.gs_gray::text')[1].get(),
            #         'volume': title.css('.gsc_a_y span::text').get(),
            #         }
            # else:
            #     yield{
            #         'tiltle': title.css('a.gsc_a_at::text').get(),
            #         'authors': title.css('.gs_gray::text')[0].get()
            #     }
                yield scrapy.Request(
                    url = response.urljoin(self.index + title.css('a.gsc_a_at::attr(href)').get()),
                    callback= self.paper_page,
                    cb_kwargs=dict(title=title.css('a.gsc_a_at::text').get().replace(':',''))
                )
        if load_more:
            url=response.urljoin(
                f'https://scholar.google.com/citations?user={self.author}&hl=en&oi=ao&cstart={self.start_page}&pagesize={self.page_size}')
            self.start_page += self.page_size
            self.page_size=100
            yield scrapy.FormRequest(url, method='POST', callback=self.parse)
    def paper_page(self, response, title):
        pdf_url=response.css('div.gsc_oci_title_ggi a::attr(href)').get()
        yield scrapy.Request(
            url=response.urljoin(pdf_url),
            callback=self.save_pdf,
            cb_kwargs=dict(title=title)
        )
    def save_pdf(self, response, title):
        if not self.paper_dir_parent.is_dir():
            self.paper_dir_parent.mkdir()
        if not self.paper_dir.is_dir():
            self.paper_dir.mkdir()
        path=response.url.split('/')[-1]
        self.logger.info('Saving PDF %s', path)
        save_dir=Path(self.paper_dir, title + '.pdf')
        print(f'Saving PDF {str(save_dir)}')
        if not save_dir.is_file():
            with open(save_dir, 'wb') as f:
                f.write(response.body)
