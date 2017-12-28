from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import time

print('Python is Awesome')

URL = 'https://www.screener.in/'

# Start the WebDriver and load the page
wd = webdriver.Chrome('C:\\Coding\\WebDriver\\chromedriver.exe')
wd.set_page_load_timeout(30)
wd.get(URL)
#wd.maximize_window()
### Enter in search bar the stock name
StockName = 'Sampre'
wd.find_element_by_xpath("//input[@class='form-control']").send_keys(StockName)
time.sleep(1)
wd.find_element_by_xpath("//li[@class='active']").click()
URL = wd.current_url
wd.quit()

print('Opening :' + URL)
wd = webdriver.Chrome('C:\\Coding\\WebDriver\\chromedriver.exe')
wd.get(URL)
time.sleep(2)
html_page  = wd.page_source

soup = BeautifulSoup(html_page,'html.parser')
#print(soup.prettify())
allDetails = soup.find_all('h4', class_="col-sm-4")
for idx,item in enumerate(allDetails):
    if(idx <= 8):
        print(str(idx) + item.text.strip())

wd.quit()
