from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys

# 1. Khai bao bien browser
browser = webdriver.Chrome(executable_path='chromedriver.exe')

# 2. Mo thu mot trang web
browser.get('https://www.facebook.com/')

# 2a. Dien thong tin vao o user va pass
txtUser = browser.find_element_by_id('email')
txtUser.send_keys('lenguyenhoangmai2001@gmail.com')

txtPass = browser.find_element_by_id('pass')
txtPass.send_keys('akira kurusu')

# 2b. Submit form
txtPass.send_keys(Keys.ENTER)


# 3. Dung chuong trinh 5s
sleep(5)

# 4. Dong trinh duyet
browser.close()
