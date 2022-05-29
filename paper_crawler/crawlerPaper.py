from operator import imod
from bs4 import BeautifulSoup
from selenium import webdriver
import json


options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("D:/Ki_6/PR/Crawler/new_crawl/chromedriver.exe", chrome_options=options)

def get_href(source):
    driver.get(source)

    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'html.parser')
    hrefs = []
    next_page = None
    for i in range(20):
        papers_selector = soup.find_all('li', class_='search__item issue-item-container')
        for paper_selector in papers_selector:
            href_span = paper_selector.find('span', class_="hlFld-Title")
            href = href_span.find('a', class_= '').get('href')
            href = href.strip()
            hrefs.append(href)
        try:
            next_page = driver.find_element_by_xpath('//*[@id="pb-page-content"]/div/main/div[1]/div/div[2]/div/nav/span/a/@href')
        except:
            pass
        if next_page == None:
            break
        next_page.click()

    return hrefs

def extract_data(href):
    driver.get("https://dl.acm.org" + href)

    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'html.parser')

    title = soup.find('h1', class_= 'citation__title').getText()

    authors_selector = soup.find_all('li', class_="loa__item")
    authors = []
    for author_selector in authors_selector:
        author = author_selector.find('span', class_='').getText()
        author = author.strip()
        authors.append(author)

    abstract = soup.find('div', class_="abstractSection abstractInFull").getText()
    conference = soup.find('span', class_='epub-section__title').getText()

    paper_data = {'title': title,
                'authors': authors,
                'abstract': abstract,
                'conference': conference}

    return paper_data

source = 'https://dl.acm.org/action/doSearch?AllField=Ngo+Duc+Thanh'
file_name = 'paper.json'
f = open(file_name, 'w')
hrefs = get_href(source)
data = []
for no in range(len(hrefs)):
    href = hrefs[no]
    paper_data = extract_data(href)
    data.append(paper_data)
json.dump(data, f, indent=4)
f.close()
