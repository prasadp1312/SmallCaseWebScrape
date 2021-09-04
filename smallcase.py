from selenium import webdriver
import time
from bs4 import BeautifulSoup


def countdown(start=30, end=0):
    """Update to print every 5 sec in between"""
    print("Login with in " + str(start) + " seconds")
    time.sleep(start)
    print(str(start) + " Done ...")


class SmallCase:
    """get data from www.smallcase.com"""

    Driver = 'D:\\GitHub\\chromedriver.exe'  # Update with chrome driver location V92.0.
    ZerodhaUrl = 'https://smallcase.zerodha.com/discover/all?count=31'  # Update with broker URL
    wd = []
    scName = []
    scLink = []
    scStock = []
    htmlpage = ""
    soup = ""

    def __init__(self):
        self.logintozerodhasmallcase()
        self.html_page = self.wd.page_source
        # self.mockMainPage() # Copy results and save in a txt file
        self.soup = BeautifulSoup(self.html_page, 'html.parser')
        self.getallsmallcase()
        self.getallsmallcaselinks()
        for idx, links in enumerate(self.scLink):
            self.getdatafromsmallcase(links)

    def logintozerodhasmallcase(self):
        print("login to small case with your zerodha account")
        self.wd = webdriver.Chrome(self.Driver)
        self.wd.set_page_load_timeout(30)
        self.wd.get(self.ZerodhaUrl)
        """ Automate login with encrypted Credentials """
        countdown()

    def getallsmallcase(self):
        titlename = "SmallcaseCard__title__2M7E_ line-height-one ellipsis mr8 SmallcaseCard__size-auto__NxnIC"
        allsc = self.soup.findAll(class_=titlename)
        for idx, data in enumerate(allsc):
            # print(data.string)
            self.scName.append(data.string)

    def getallsmallcaselinks(self):
        linkmatch = "SmallcaseCard__description__1H-JL text-14 text-normal lh-157 mb8 SmallcaseCard__size-auto__NxnIC"
        allsclink = self.soup.select(
            'p[class*="SmallcaseCard__description__1H-JL text-14 text-normal lh-157 mb8 '
            'SmallcaseCard__size-auto__NxnIC"]')
        sclinklist = allsclink[0:len(allsclink)]
        for idx, data in enumerate(sclinklist):
            # Find link extension from 'js-shave_(.+?)'
            liskprefix = 'https://smallcase.zerodha.com/smallcase/'
            replacetolink = 'class="js-shave_'  # Get link from end of js-shave_
            linkpostfix = '/stocks'
            data = str(data)
            data = data.split()
            data = data[1]
            # print(data.replace(replaceToLink,liskPrefix)+linkPostFix)
            self.scLink.append(data.replace(replacetolink, liskprefix) + linkpostfix)

    def getdatafromsmallcase(self, sclink):
        print(sclink)
        self.wd.get(sclink)
        self.html_page = self.wd.page_source
        self.soup = BeautifulSoup(self.html_page, 'html.parser')
        # print(self.soup)
        self.getstockdatafromsmallcase()

    def getstockdatafromsmallcase(self):
        time.sleep(2)
        stock = []
        segment = []
        titlename = "StocksWeights__stock-name__2ANv4 pull-left font-medium text-14 text-blue ellipsis"
        allsc = self.soup.findAll(class_=titlename)
        for idx, data in enumerate(allsc):
            print(data.string)
            stock.append(data.string)

        self.scStock.append(stock)
        segmentsname = "ellipsis"
        allsc = self.soup.findAll(class_=segmentsname)
        for idx, data in enumerate(allsc):
            # print(data.string)
            segment.append(data.string)

        # segment = set(segment) - set(stock)
        # print(segment)

    def mockmainpage(self):
        f = open("MainPageSample.html", "r")
        self.html_page = f.read()
        f.close()

# Driver Code
# TODO : Implement Write to file
# TODO : Implement max repeats


sc = SmallCase()
