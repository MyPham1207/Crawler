from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
import csv

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome('D:/Hoc/HK6/NhanDang/Crawler/Image_Crawler/chromedriver.exe', chrome_options=options)

def Find_link():
  driver.get("https://vnexpress.net")
  more_buttons = driver.find_elements_by_class_name("more")
  for x in range(len(more_buttons)):
    if more_buttons[x].is_displayed():
        driver.execute_script("arguments[0].click();", more_buttons[x])
        time.sleep(1)
  page_source = driver.page_source


  soup = BeautifulSoup(page_source, 'html.parser')


  Links = soup.find('section', class_='section section_topstory').find_all('h3')
  print(Links)
  for link in Links:
    print(link.find('a').get('href'))
  return Links

def CrawlNews(Links):
  for i in range(len(Links)):
    driver.get(Links[i].find('a').get('href'))
    more_buttons = driver.find_elements_by_class_name("more")
    for x in range(len(more_buttons)):
      if more_buttons[x].is_displayed():
          driver.execute_script("arguments[0].click();", more_buttons[x])
          time.sleep(1)
    url = driver.page_source

    # url =  'https://vnexpress.net/95-dan-so-se-duoc-phu-bao-hiem-y-te-nam-2025-4458445.html'
    # page = urllib.request.urlopen(url)

    soup = BeautifulSoup(url,'html.parser')
    try:
      new_feeds = soup.find('section', class_="section page-detail top-detail").find_all('p',class_="Normal")
      title = soup.find('section', class_="section page-detail top-detail").find('h1',class_="title-detail")
      date = soup.find('section', class_="section page-detail top-detail").find('span',class_="date")
      des = soup.find('section', class_="section page-detail top-detail").find('p',class_="description")
      comments = soup.find('section', class_='section page-detail middle-detail').find_all('p')
    except:
      pass


    with open('news_data{}.csv'.format(i), 'w', encoding="utf-8") as csv_file:
      writer = csv.writer(csv_file)
      writer.writerow(['Tilte:'])
      writer.writerow([title.getText()])
      writer.writerow(['Date & Time:'])
      writer.writerow([date.getText()])
      writer.writerow(['Descripton:'])
      writer.writerow([des.getText()])
      writer.writerow(['Content:'])
      for feed in new_feeds:
        writer.writerow([feed.getText()])
      writer.writerow(['Comment'])
      for comment in comments:
        writer.writerow([comment.getText()])


Links=Find_link()
CrawlNews(Links)