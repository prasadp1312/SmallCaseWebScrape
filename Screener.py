from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import time

Driver = 'D:\\Coding\\WebDriver\\chromedriver.exe'
def getValuesScreener(StockName,Extension):
    URL = 'https://www.screener.in/company/' + StockName + '/' + Extension
    print(' Opening : ' + URL)
    wd = webdriver.Chrome(Driver)
    wd.get(URL)
    wd.set_window_size(0, 0)
    time.sleep(1)
    html_page = wd.page_source
    wd.quit()
    return(html_page)

def getIndividualValues(soup):
    Values = []
    allDetails = soup.find_all('h4', class_="col-sm-4")
    for idx, item in enumerate(allDetails):
        Values.append(item.text.split())

    Data = []
    if '--' not in Values[0][2]:
        Data.append(str(Values[0][3]).replace(',',''))
    else:
        Data.append('No-Data')

    if '--' not in Values[1][2]:
        Data.append(str(Values[1][3]).replace(',',''))
    else:
        Data.append('No-Data')

    if '--' not in Values[2][2]:
        Data.append(str(Values[2][3]).replace(',',''))
    else:
        Data.append('No-Data')

    if '--' not in Values[3][2]:
        Data.append(str(Values[3][2]).replace(',',''))
    else:
        Data.append('No-Data')

    if '--' not in Values[4][2]:
        Data.append(str(Values[4][2]).replace(',',''))
    else:
        Data.append('No-Data')

    if '--' not in Values[5][2]:
        Data.append(str(Values[5][3]).replace(',',''))
    else:
        Data.append('No-Data')

    if 'NaN' not in Values[8][4]:
        Data.append(str(Values[8][4]).replace(',',''))
    else:
        Data.append('No-Data')

    if 'NaN' not in Values[8][7]:
        Data.append(str(Values[8][7]).replace(',',''))
    else:
        Data.append('No-Data')

    return Data


def scrapeScreener(StockTicker):
    html_page = getValuesScreener(StockTicker,'consolidated')
    soup = BeautifulSoup(html_page, 'html.parser')
    Values = getIndividualValues(soup)
    if 'No-Data' in Values:
        print('No Values found, Retrying')
        html_page = getValuesScreener(StockTicker,'')
        soup = BeautifulSoup(html_page, 'html.parser')
        Values = getIndividualValues(soup)
        return Values
    else:
        print('Values found')
        return Values

