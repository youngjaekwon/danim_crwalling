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

option = webdriver.ChromeOptions()
option.add_argument('--window-size=1920x1080')
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

url = 'https://the35mm.com/product/list.html?cate_no=24'
driver.get(url)
time.sleep(3)

aTagListSize = len(driver.find_elements(By.CSS_SELECTOR, '.prdImg > a'))
time.sleep(2)
categoryCol = []
companyCol = []
nameCol = []
expCol = []
priceCol = []
picCol = []
for x in range(0, aTagListSize):
    a = driver.find_elements(By.CSS_SELECTOR, '.prdImg > a')[x]
    a.send_keys(Keys.ENTER)
    time.sleep(2)

    # html 받아오기
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    categoryCol.append('Film Camera')
    text = soup.find('tr', class_='xans-record-').find('td').find('span').decode_contents(formatter='html')
    textList = text.split('<br/>')
    companyCol.append(textList[0])
    nameCol.append(textList[1])
    if len(textList) > 2:
        expCol.append(textList[2])
    else:
        expCol.append('')
    priceCol.append(soup.find_all('tr', class_='xans-record-')[1].find('td').find('span').get_text())
    picList = ""
    picList += "https:" + soup.find('img', class_='BigImage')['src']
    imgRS = soup.find_all('img', class_='ThumbImage')
    for j in range(1, len(imgRS)):
        picList += "$https:" + imgRS[j]['src']
    picCol.append(picList)
    driver.execute_script("window.history.go(-1)")
    time.sleep(2)

raw_data = {'카테고리': categoryCol,
            '제조사': companyCol,
            '제품명': nameCol,
            '설명': expCol,
            '가격': priceCol,
            '사진': picCol}

df = pd.DataFrame(raw_data)
df.to_csv('filmCamera.csv')