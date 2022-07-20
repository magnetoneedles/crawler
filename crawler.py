import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import time
import threading



# Декоратор для потоков
def thread(my_func):
    def wrapper(*args, **kwargs):
        my_thread = threading.Thread(target=my_func, args = args, kwargs=kwargs)
        my_thread.start()
    return wrapper

# Инициализировать набор ссылок (уникальные ссылки)
int_url = []
ext_url = set()

# Проверяем URL
def valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

# Возвращаем все URL-адреса

def website_links(url):
    urls = []
    # извлекаем доменное имя из URL
    domain_name = urlparse(url).netloc
    # скачиваем HTML-контент вэб-страницы
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    # Теперь получим все HTML теги, содержащие все ссылки  вэб-страницы
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href пустой тег
            continue
        # присоединить URL, если он относительный (не абсолютная ссылка)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # удалить параметры URL GET, фрагменты URL и т. д.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        # Завершаем функцию.
        # Если URL-адрес недействителен  или  если URL уже находится в int_url , следует перейти к следующей ссылке.
        # Если URL является внешней ссылкой, вывести его и добавить в глобальный набор ext_url и перейдти к следующей ссылке.
        # И наконец, после всех проверок  получаем URL, являющийся  внутренней ссылкой; выводим ее и добавляем в наборы urls и int_url
        if not valid_url(href):
            # недействительный URL
            continue
        if href in int_url:
            # уже в наборе
            continue
        if domain_name not in href:
            # внешняя ссылка
            if href not in ext_url:
                ext_url.add(href)
            continue
        urls.append(href)
        int_url.append(href)
    return urls



def double_examination(mas):
    counter = 0
    for el in range(0,len(mas)):
        for cursor in range(el+1,len(mas)):
            if mas[el] == mas[cursor]:
                counter+=1
    return counter

pages_to_parse=['http://crawler-test.com/']
parsed_pages=[]
site_links=[]



def crawler(a):
    while pages_to_parse != []:
        start = time.time()
        current_page = pages_to_parse.pop()
        print(current_page)
        print(double_examination(int_url))
        website_links(current_page)
        parsed_pages.append(current_page)
        for element in int_url:
            if element not in parsed_pages:
                pages_to_parse.append(element)
        end = time.time()
        print(end-start)

for url in pages_to_parse:
    threading.Thread(target = website_links, args=url.start())

    





        




""" class Crawler:

    def __init__(self, page_to_parse):
        self.page_to_parse = page_to_parse
        self.pages_to_parse = [self.page_to_parse]
        self.site_links = []

    def valid_url(url):
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def website_links(url):
        for url in self.pages_to_parse:
            
        urls = []
        # извлекаем доменное имя из URL
        domain_name = urlparse(url).netloc
        # скачиваем HTML-контент вэб-страницы
        soup = BeautifulSoup(requests.get(url).content, "html.parser")
        # Теперь получим все HTML теги, содержащие все ссылки  вэб-страницы
        for a_tag in soup.findAll("a"):
            href = a_tag.attrs.get("href")
            if href == "" or href is None:
                # href пустой тег
                continue
            # присоединить URL, если он относительный (не абсолютная ссылка)
            href = urljoin(url, href)
            parsed_href = urlparse(href)
            # удалить параметры URL GET, фрагменты URL и т. д.
            href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
            # Завершаем функцию.
            # Если URL-адрес недействителен  или  если URL уже находится в int_url , следует перейти к следующей ссылке.
            # Если URL является внешней ссылкой, вывести его и добавить в глобальный набор ext_url и перейдти к следующей ссылке.
            # И наконец, после всех проверок  получаем URL, являющийся  внутренней ссылкой; выводим ее и добавляем в наборы urls и int_url
            if not valid_url(href):
                # недействительный URL
                continue
            if href in int_url:
                # уже в наборе
                continue
            if domain_name not in href:
                # внешняя ссылка
                if href not in ext_url:
                    ext_url.add(href)
                continue
            urls.append(href)
            int_url.append(href)
        return urls """

    


