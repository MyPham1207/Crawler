from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import json

# 1. Khai bao browser
browser = webdriver.Chrome(service=Service('chromedriver.exe'))

browser.get("https://m.facebook.com/ConfessionUIT/")

loginButton = browser.find_element(by=By.XPATH, value="//*[text()='Log In']")
loginButton = loginButton.find_element(by=By.XPATH, value="./..")
loginButton.click()
sleep(random.randint(5,10))

txtUser = browser.find_element(by=By.NAME, value="email")
txtUser.send_keys('your_username')

txtPass = browser.find_element(by=By.NAME, value="pass")
txtPass.send_keys('your_password')

# 2b. Submit form
txtPass.send_keys(Keys.ENTER)

# 3. Dung chuong trinh
sleep(random.randint(10, 15))

SCROLL_PAUSE_TIME = 5

# source
# Get scroll height
last_height = browser.execute_script("return document.body.scrollHeight")

for _ in range(10):
    # Scroll down to bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

posts = browser.find_elements(by=By.CSS_SELECTOR, value="div[class='story_body_container'] > div > a")
post_links = [post.get_attribute('href') for post in posts]


def crawl(post_link, post_num):
    # 2a. Mo URL cua post
    browser.get(post_link)
    sleep(random.randint(5,10))

    # 4. Lay content cua post
    postContent = browser.find_element(by=By.CSS_SELECTOR, value="div[class='story_body_container'] > div:nth-child(2) > div > p")
    fo = open('post\post{}_content.txt'.format(post_num), 'w', encoding='utf-8')
    fo.write(postContent.text)

    # Nhan xem them binh luan 1 lan, de vong for de co the bo qua cau lenh nay neu khong co nut xem them binh luan
    for _ in range(1):
        try:
            showmoreLink = browser.find_element(by=By.CSS_SELECTOR, value = "div[id*='see_next'] > a")
            showmoreLink.click()
            sleep(random.randint(1, 5))
        except:
            continue

    sleep(random.randint(10, 15))
    # 5. Tim tat ca cac comment va ghi ra file
    commentList = browser.find_elements(by=By.CLASS_NAME, value="_14v5")

    fo = open('comment\comment_post{}.json'.format(post_num), 'w', encoding='utf-8')
    cmtList = []

    # 6. Lap trong tat ca cac comment va lay nguoi comment cung nhu noi dung comment
    for comment in commentList:
        try:
            cmter = comment.find_element(by=By.CSS_SELECTOR, value="div > div:first-child > a")
            cmtContent = comment.find_element(by=By.CSS_SELECTOR, value="div > div[data-sigil='comment-body']")
            cmtList.append({"Name": cmter.text, "Content": cmtContent.text})
        except:
            continue
    json.dump(cmtList, fo, ensure_ascii=False, indent=4)

    fo.close()

# Main
for post_num in range(len(post_links)):
    crawl(post_links[post_num], post_num)

browser.close()
