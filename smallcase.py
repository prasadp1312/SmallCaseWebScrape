from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time

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
#wd.quit()

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


for allStkSc in range(len(scLink)):
    print('########################################')
    print(scName[allStkSc])
    print('########################################')
    wd.get(scLink[allStkSc])
    html_page  = wd.page_source
    #wd.quit()

    soup = BeautifulSoup(html_page,'html.parser')
    #print(soup.prettify())

    print('$$$ Segment -->')
    allSc = soup.find_all(class_="segment-name")
    for idx,sc in enumerate(allSc):
            print(idx,sc.string)

    print('\n$$$ Stocks --->')
    allSc = soup.find_all("tip-cont")
    for idx,sc in enumerate(allSc):
            print(idx,sc.string)
