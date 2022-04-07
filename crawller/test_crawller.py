from xml.etree.ElementPath import xpath_tokenizer
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import time
import pandas as pd

driver = webdriver.Chrome(
    executable_path='/Users/yjkwon/Downloads/chromedriver')
driver.implicitly_wait(3)
act = ActionChains(driver)
SCROLL_PAUSE_SEC = 3
# headless option
# chromedriver = '/Users/yjkwon/Downloads/chromedriver'
# headless_options = webdriver.ChromeOptions()
# headless_options.add_argument('headless')
# driver = webdriver.Chrome(chromedriver, options=headless_options)

url = 'https://www.tripadvisor.co.kr/Tourism-g294197-Seoul-Vacations.html#/media/294197/'
driver.get(url)
time.sleep(3)

# url list
urls = []

# html 받아오기
# html = driver.page_source
# soup = BeautifulSoup(html, 'html.parser')

# for pic in soup.find('div', class_='bMLNe').find_all('picture'):
#     print(pic.find('img')['srcset'])
#     print()

# 스크롤 다운 1000px
scroll = driver.find_element(
    By.CSS_SELECTOR, '#lithium-root > main > div.bzEkR._T > div > div > div.cYmkE.t.s.l._U > div > div.dzySL.z.t.l.s._U._f > div:nth-child(2) > div > div.eSdUb.f > div > div > div.Pksol._R.z')
time.sleep(5)
driver.execute_script("arguments[0].scrollBy(0, 1000)", scroll)
time.sleep(5)

# html 받아오기
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# img url을 list에 저장하기
for pic in soup.find('div', class_='bMLNe').find_all('picture'):
    urls.append(pic.find('img')['srcset'])

# 스크롤 1000px
driver.execute_script("arguments[0].scrollBy(0, 1000)", scroll)
time.sleep(5)

# html 받아오기
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# img url을 list에 저장하기
for pic in soup.find('div', class_='bMLNe').find_all('picture'):
    urls.append(pic.find('img')['srcset'])

time.sleep(5)

# data frame 생성
df = pd.DataFrame(urls)

# column명 지정
df.columns = ["url"]

# cvs파일로 저장
df.to_csv("url.csv")

# driver.execute_script("arguments[0].scrollBy(0, 5000)", scroll)
# time.sleep(10)

# html = driver.page_source
# soup = BeautifulSoup(html, 'html.parser')

# for pic in soup.find('div', class_='bMLNe').find_all('picture'):
#     print(pic.find('img')['srcset'])
#     print()
