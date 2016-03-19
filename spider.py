from urllib.request import urlopen
from urllib.request import FancyURLopener

from link_hunter import LinkHunter
from general import *
import sys

class MyOpener(FancyURLopener):
    version = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'


class Spider:

    # class variables which are shared among all instances
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    #the sets are essentially used while the bot is running
    #once program finishes it stores to hdd using the files defined above
    queue_set = set()
    crawled_set = set()

    def __init__(self, project_name, base_url, domain_name):
        #this ensures that all spiders have the same SHARED information
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        self.boot()
        self.crawl_page('first!', Spider.base_url)

    @staticmethod
    def boot():
        create_project_directory(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)

        Spider.queue_set = file_to_set(Spider.queue_file)
        Spider.crawled_set = file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled_set:
            print(thread_name + 'crawling ' + page_url)
            print('Queue items left: ' + str(len(Spider.queue_set)))
            print('Crawled items left: ' + str(len(Spider.crawled_set)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue_set.remove(page_url)
            Spider.crawled_set.add(page_url)
            Spider.update_files()

    @staticmethod
    def add_links_to_queue(links):
        for link in links:
            if link in Spider.queue_set:
                continue
            if link in Spider.crawled_set:
                continue
            if Spider.domain_name not in link:
                continue

            Spider.queue_set.add(link)

    @staticmethod
    def gather_links(page_url):

        html_string = ''
        try:
            myopener = MyOpener()
            response = myopener.open(page_url)
            # response = urlopen(page_url)

            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode('utf-8')
            finder = LinkHunter(Spider.base_url, page_url)
            finder.feed(html_string)
        except:
            e = sys.exc_info()[0]
            print('Error: can\'t crawl page!')
            print(e)
            return set()
        return finder.page_links()

    @staticmethod
    def update_files():
        set_to_file(Spider.queue_set, Spider.queue_file)
        set_to_file(Spider.crawled_set, Spider.crawled_file)























