from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import time
import NseTicker
import Screener

# Finding Nummbers as String from Screener
def find_numbers(string, ints=True):
    numexp = re.compile(r'[-]?\d[\d,]*[\.]?[\d{2}]*') #optional - in front
    numbers = numexp.findall(string)
    return(numbers)

Driver = 'D:\\Coding\\WebDriver\\chromedriver.exe'
start_time = time.time()
print('Python is Awesome')

URL = 'https://www.smallcase.com/discover?sortBy=Latest&count=100'

# Start the WebDriver and load the page
wd = webdriver.Chrome(Driver)
wd.set_page_load_timeout(30)
wd.get(URL)
html_page  = wd.page_source

### Find Login Button & Click -- Opnes New Window
#wd.find_element_by_xpath("//button[@class='btn btn-lg btn-secondary kite-login']").click()

scName = []
scLink = []
scNameLinkFile = open('ScNameLink.csv','w')
scStocksFile = open('ScStocks.csv','w', encoding="utf-8")
stocksList = open('OnlyStocksList.csv','w', encoding="utf-8")
soup = BeautifulSoup(html_page,'html.parser')
#print(soup.prettify())

allSc = soup.find_all(class_="name pull-left")
for idx,sc in enumerate(allSc):
    scName.append(sc.string)

# Find all Links with text '/smallcase/ anywhere between it
allScLinks = soup.findAll('a', attrs={'href': re.compile("^/smallcase/")})

for idx,link in enumerate(allScLinks):
    scIndivLink = link.get('href')
    scLink.append('https://www.smallcase.com/smallcase/stocks' + scIndivLink[10:20])

scNameLinkFile.write('SmallCaseName , SmallcaseLink'+ '\n')
for iter in range(len(allScLinks)):
    print(scName[iter] + ',' + scLink[iter] + '\n')
    scNameLinkFile.write(scName[iter] + ',' + scLink[iter] + '\n')

scNameLinkFile.close()

print('Please Login Within 30 Seconds :')
time.sleep(30)

scSegments = []
scStocks= []
scStocksTickr = []
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
        if sc.string is not None:
            scSegments.append(sc.string)
            print(idx,sc.string)

    print('\n$$$ Stocks --->')
    allSc = soup.find_all("tip-cont")
    for idx,sc in enumerate(allSc):
        if sc.string is not None:
            scStocks.append((sc.string))
            print(idx,sc.string)

stop_time = time.time()
print('Time Taken = ' + str(int(stop_time - start_time - 20)) + ' Seconds to scrape ' + str(len(scStocks)) + ' stocks from ' + str(len(scName)) + ' Smallcases')
scStocks = list(set(scStocks))
print('Non Duplicate Stocks : ' + str(len(scStocks)))
for stocks in scStocks:
    if stocks is not None :
        StockTickr = NseTicker.getTicker(stocks)
        scStocksTickr.append(StockTickr)
        print(stocks + ' --> ' + StockTickr)
        stocksList.write(stocks + ',' + StockTickr + '\n')
wd.quit()
stocksList.close()

start_time = time.time()
scStocksFile.write('Stocks,Ticker,Market Cap,Current Price,Book Value,Stock PE,Dividend Yield,Face Value,52Wk High,52Wk Low,Screener Link'+ '\n')
for itr in range(len(scStocks)):#len(scStocks)
    StockTickr = scStocksTickr[itr]
    StockName = scStocks[itr]

    if StockName is not None and  StockTickr is not None:
        print('#' + str(itr) + '/' + str(len(scStocks))+ ' : ' +StockName + '->'+ StockTickr )
    else:
        print('Something is Wrong in' + str(itr))
        continue

    scStocksFile.write(StockName + ',' + StockTickr + ',')
    data = Screener.scrapeScreener(StockTickr)
    print(data)
    scStocksFile.write(data[0] + ',' + data[1] + ',' +data[2] + ',' +data[3] + ',' +data[4] + ',' +data[5] + ',' +data[6] + ',' +data[7] + '\n' )

scStocksFile.close()
wd.quit()
stop_time = time.time()
print('Time Taken = ' + str(int(stop_time - start_time)) + 'Seconds')
