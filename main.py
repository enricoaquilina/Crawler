import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *


PROJECT_NAME = 'science'
HOME_PAGE = 'http://sciencealert.com'
DOMAIN_NAME = get_domain_name(HOME_PAGE)

QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8

queue = Queue()
Spider(PROJECT_NAME, HOME_PAGE, DOMAIN_NAME)

# If there are items in the queue
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    link_no = len(queued_links)
    if link_no > 0:
        print(str(link_no) + 'links remaining...')
        create_jobs(queued_links)

def create_jobs(queued_links):
    for link in queued_links:
        queue.put(link)
    # prevent race conditions
    # tell thread to 'wait its turn'
    queue.join()
    crawl()

def create_spiders():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        # ensures that its a daemon process and dies with main
        t.daemon = True
        t.start()

# assign work to the spiders
def work():
    while True:
        link = queue.get()
        Spider.crawl_page(threading.current_thread().name, link)
        queue.task_done()

create_spiders()
crawl()