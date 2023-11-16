""""
This function is used to scrap historical stock price from Yahoo finance. It will scraped all data displayed on the website.
-----
Parameters :
    company : str
-----
Examples:
yahoo_scraper('apple')
            Date    Open    High     Low   Close Adj Close     Volume
0    Dec 15 2022  141.11  141.80  136.03  136.50    136.50   98822900
1    Dec 14 2022  145.35  146.66  141.16  143.21    143.21   82291200
2    Dec 13 2022  149.50  149.97  144.24  145.47    145.47   93886200
3    Dec 12 2022  142.70  144.50  141.06  144.49    144.49   70462700
4    Dec 09 2022  142.34  145.57  140.90  142.16    142.16   76069500
..           ...     ...     ...     ...     ...       ...        ...
247  Dec 22 2021  173.04  175.86  172.15  175.64    174.63   92135300
248  Dec 21 2021  171.56  173.20  169.12  172.99    171.99   91185900
249  Dec 20 2021  168.28  170.58  167.46  169.75    168.77  107499100
250  Dec 17 2021  169.93  173.47  169.69  171.14    170.15  195432700
251  Dec 16 2021  179.28  181.14  170.75  172.26    171.27  150185800
[252 rows x 7 columns]

"""

import pandas as pd
import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.common.by import By


def yahoo_scraper(company):
    # Clicking "Submit" button
    driver = webdriver.Chrome()
    URL = "https://finance.yahoo.com/"
    driver.get(URL)
    time.sleep(2)
    #close the free trial window
    driver.find_element(by=By.XPATH,value = "/html/body/div[1]/div/div/div[1]/div/div[4]/div/div/div[1]/div/div/div/div/div/button").click()
    time.sleep(1)
    # Enter name of company in searchbox, and wait for 2 seconds.
    driver.find_element(by=By.XPATH,value = "/html/body/div[1]/div/div/div[1]/div/div[1]/div[1]/div/div/div[1]/div/div/div/div[1]/div/div[2]/div/form/input[1]").send_keys(company)
    time.sleep(2)
    # Click on Search icon and wait for 2 seconds.
    #find_element is the new script of driver after edition 4.3 or something
    driver.find_element(by = By.XPATH, value= "/html/body/div[1]/div/div/div[1]/div/div[1]/div[1]/div/div/div[1]/div/div/div/div[1]/div/div[2]/div/form/div[1]").click()
    time.sleep(2)
    #close the sign in window
    driver.find_element(by = By.XPATH, value= "/html/body/div[1]/div/div/div[1]/div/div[4]/div/div/div[1]/div/div/div/div/div/section/button[1]").click()
    time.sleep(1)
    # Driver clicks on Historical Data tab and sleeps for 2 seconds.
    driver.find_element(by= By.XPATH, value = "//span[text() = 'Historical Data']").click()
    time.sleep(2)
    # Driver scrolls down three times to load the table.
    for i in range(0,3):
         driver.execute_script("window.scrollBy(0,5000)")
         time.sleep(2)
    # Web page fetched from driver is parsed using Beautiful Soup.
    #Turn str into beautifulsoup object
    HTMLPage = BeautifulSoup(driver.page_source, 'html.parser')
    # Table is searched using class and stored in another variable.
    Table = HTMLPage.find('table', class_='W(100%) M(0)')
    # List of all the rows is store in a variable 'Rows'.
    Rows = Table.find_all('tr', class_='BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)')

    extracted_data = []
    for i in range(0, len(Rows)):
        try:
            column = {}
            Values = Rows[i].find_all('td')
        # Values (Open, High, Close etc.) are extracted and stored in dictionary
            if len(Values) == 7:
                column["Date"] = Values[0].find('span').text.replace(',', '')
                column["Open"] = Values[1].find('span').text.replace(',', '')
                column["High"] = Values[2].find('span').text.replace(',', '')
                column["Low"] = Values[3].find('span').text.replace(',', '')
                column["Close"] = Values[4].find('span').text.replace(',', '')
                column["Adj Close"] = Values[5].find('span').text.replace(',', '')
                column["Volume"] = Values[6].find('span').text.replace(',', '')
                extracted_data.append(column)
        except:
            # To check the exception caused for which company
            print("Row Number: " + str(i))
        finally:
        # To move to the next row
            i = i + 1

    # Converted list of dictionaries to a Dataframe.
    extracted_data = pd.DataFrame(extracted_data)
    print(extracted_data)
