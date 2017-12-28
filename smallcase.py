from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import time

start_time = time.time()
print('Python is Awesome')

URL = 'https://www.smallcase.com/discover?sortBy=Latest&count=100'

# Start the WebDriver and load the page
wd = webdriver.Chrome('C:\\Coding\\WebDriver\\chromedriver.exe')
wd.set_page_load_timeout(30)
wd.get(URL)
#wd.maximize_window()
html_page  = wd.page_source

### Find Login Button & Click -- Opnes New Window
#wd.find_element_by_xpath("//button[@class='btn btn-lg btn-secondary kite-login']").click()

scName = []
scLink = []

soup = BeautifulSoup(html_page,'html.parser')
#print(soup.prettify())

allSc = soup.find_all(class_="name pull-left")
for idx,sc in enumerate(allSc):
    scName.append(sc.string)
    print(scName[idx])

allScLinks = soup.findAll('a', attrs={'href': re.compile("^/smallcase/")})

for idx,link in enumerate(allScLinks):
    scIndivLink = link.get('href')
    scLink.append('https://www.smallcase.com/smallcase/stocks' + scIndivLink[10:20])
    print(scLink[idx])

print('Please Login Within 30 Seconds :')
time.sleep(30)

scSegments = []
scStocks= []
for allStkSc in range(len(scLink)):
    print('########################################')
    print(scName[allStkSc])
    print('########################################')
    wd.get(scLink[allStkSc])
    html_page  = wd.page_source
    #wd.quit()

    soup = BeautifulSoup(html_page,'html.parser')
    #print(soup.prettify())

    allSc = soup.find_all(class_="value-wrap value text-success")
    for idx,sc in enumerate(allSc):
        scSegments.append(sc.string)
        print(idx,sc.string)

    print('$$$ Segment -->')
    allSc = soup.find_all(class_="segment-name")
    for idx,sc in enumerate(allSc):
        scSegments.append(sc.string)
        print(idx,sc.string)

    print('\n$$$ Stocks --->')
    allSc = soup.find_all("tip-cont")
    for idx,sc in enumerate(allSc):
        scStocks.append((sc.string))
        print(idx,sc.string)

stop_time = time.time()
print('Time Taken = ' + str(int(stop_time - start_time - 20)) + ' Seconds to scrape ' + str(len(scStocks)) + ' stocks from ' + str(len(scName)) + ' Smallcases')
repeats = [[x,scStocks.count(x)] for x in set(scStocks)]
for stocks in repeats:
    print(stocks)
scStocks = list(set(scStocks))
print('Non Duplicate Stocks : ' + str(len(scStocks)))
for stocks in scStocks:
    print(stocks)
wd.quit()

URL = 'https://www.screener.in/'

# Start the WebDriver and load the page
wd = webdriver.Chrome('C:\\Coding\\WebDriver\\chromedriver.exe')
wd.set_page_load_timeout(30)
wd.get(URL)
#wd.maximize_window()
### Enter in search bar the stock name
StockName = scStocks[0]
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
