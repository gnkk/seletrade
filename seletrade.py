#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support  import expected_conditions as EC
from selenium.webdriver.support.ui  import WebDriverWait
import time
import collections
import regex as re
import pandas as pd

def mojo(ticker):
    url = "https://www.marketsmojo.com/mojo/home"
    driver = webdriver.Chrome("driver/chromedriver.exe")
#     driver.maximize_window()
    driver.get(url)
    time.sleep(5)
    try:
        elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/header/div[6]/div/div/input")))
#         driver.refresh()
        for ch in list(ticker):
            elem.send_keys(ch)
            time.sleep(.1)
        time.sleep(5)    
#         elem1 = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "/html/body/div[1]/header/div[6]/div/div/ul/li[1]/a/span")))
        elem.send_keys(Keys.TAB)
        driver.find_element_by_xpath("/html/body/div[1]/header/div[6]/div/div/ul/li[1]/a/span").click()
    except Exception as e:
        print("Exception occured : 6 not found\n", e)
        elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/header/div[7]/div/div/input")))
#         driver.refresh()
        for ch in list(ticker):
            elem.send_keys(ch)
            time.sleep(.1)
        time.sleep(3)
#         elem1 = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "/html/body/div[1]/header/div[7]/div/div/ul/li[1]/a/span")))
        elem.send_keys(Keys.TAB)
        driver.find_element_by_xpath("/html/body/div[1]/header/div[7]/div/div/ul/li[1]/a/span").click()
    time.sleep(3)
    name = driver.find_element_by_class_name("mh5").text
    ltp = driver.find_element_by_class_name("mh6").text
    txt = driver.find_element_by_class_name("info-dot").get_attribute('innerHTML')
    clr = re.findall("green|orange|red|grey", txt)
    sC = collections.Counter(clr)
    score = 0+2*sC['green']+sC['orange']+20*sC['grey']
    time.sleep(6)
    driver.close()
    mojodict = {}
    mojodict['name']=name
    mojodict['ltp']=ltp
    mojodict['score']=score/8
    mojodict['clr']=clr
    return mojodict

def tline(ticker):
    url = "https://trendlyne.com/features/"
    driver = webdriver.Chrome("driver/chromedriver.exe")
#     driver.maximize_window()
    driver.get(url)
    time.sleep(5)
    elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[12]/div[1]/div[2]/div/div[1]/div/form/input")))
    elem.send_keys(ticker)
    time.sleep(3)
    driver.find_element_by_name("search").send_keys(Keys.DOWN)
    driver.find_element_by_name("search").send_keys(Keys.ENTER)
    time.sleep(5)
    score = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[1]/div/p[3]/span[1]/span").get_attribute("data-hideforvisitortitle")
    pos = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[2]/div[5]/div/a/div/div[2]/div[1]/span[1]").text
    neg = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[2]/div[5]/div/a/div/div[2]/div[3]/span[1]").text
    name = driver.find_element_by_class_name("color000000").text
    driver.close()
    try:
        fscore = str((((int(score.split("Score : ")[1][:2])+int(score.split("Score : ")[2][:2])+int(score.split("Score : ")[3][:2]))/300)+(int(pos)/(int(pos)+int(neg))))/2)
    except:
        fscore='0'
    tlinedict = {}
    tlinedict['fscore']=fscore
    tlinedict['name']=name
    return tlinedict

def ttape(ticker):
    url = "https://www.tickertape.in/"
    driver = webdriver.Chrome("driver/chromedriver.exe")
#     driver.maximize_window()
    driver.get(url)
    time.sleep(5)
    elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/header/div/div[1]/div[2]/div/div[1]/input")))
    elem.send_keys(ticker)
    time.sleep(3)
    elem.send_keys(Keys.DOWN)
    elem.send_keys(Keys.ENTER)
    time.sleep(5)

    name = driver.find_element_by_css_selector(".jsx-1914971814.stock-name.mb4.text-18.lh-138.ellipsis").get_attribute('textContent')
    i1 = driver.find_element_by_xpath("//*[@id='app-container']/div/div/div[2]/div[2]/div[3]/div[1]/div/section/div[1]/div[1]/i").get_attribute("class")
    i2 = driver.find_element_by_xpath("//*[@id='app-container']/div/div/div[2]/div[2]/div[3]/div[1]/div/section/div[1]/div[2]/i").get_attribute("class")
    i3 = driver.find_element_by_xpath("//*[@id='app-container']/div/div/div[2]/div[2]/div[3]/div[1]/div/section/div[1]/div[3]/i").get_attribute("class")
    i4 = driver.find_element_by_xpath("//*[@id='app-container']/div/div/div[2]/div[2]/div[3]/div[1]/div/section/div[1]/div[4]/i").get_attribute("class")
    i5 = driver.find_element_by_xpath("//*[@id='app-container']/div/div/div[2]/div[2]/div[3]/div[1]/div/section/div[1]/div[5]/i").get_attribute("class")
    rec = driver.find_element_by_xpath("//*[@id='app-container']/div/div/div[2]/div[2]/div[3]/div[4]/div/div[1]/div/span").text
    time.sleep(5)
    driver.close()

    txt = i1+i2+i3+i4+i5
    clr =  re.findall("positive|neutral|negative", txt)
    sC = collections.Counter(clr)
    r=re.search(r'[0-9—]*',str(rec))
    score = (((sC['positive']*2+sC['neutral'])/10)+int(re.sub('—','0',r.group(0)))/100)/2
    ttdict = {}
    ttdict['name'] = name
    ttdict['clr']=clr
    ttdict['ttscore']=score
    return ttdict

def sharescorefetch(tickerlist):
    for ticker in tickerlist:
        df = pd.DataFrame()
        print("Working on: ", ticker)
        try:
            mdict = mojo(ticker)
            ttdict = ttape(ticker)
            tldict = tline(ticker)
        except Exception as e:
            print("Exception at : ", ticker)
            print(e)
            continue
        finaldict = {}
        finaldict['name'] = str(ticker)
        finaldict['mname'] = mdict['name']
        finaldict['ttname'] = ttdict['name']
        finaldict['tlname'] = tldict['name']
        finaldict['mscore'] = mdict['score']
        finaldict['ttscore'] = ttdict['ttscore']
        finaldict['tlscore'] = tldict['fscore']
        finaldict['finalscore'] = str((float(mdict['score'])*3.5+float(tldict['fscore'])*3.5+float(ttdict['ttscore'])*3)*10)
        df = df.append(finaldict, ignore_index=True)
        print(finaldict)
        print(df)
        df.to_csv("final_jul.csv", mode='a', header=False)
        # df.to_csv("final_jul.csv")
    # return df

# file = pd.read_excel(open('stockanalyzer.xlsx', 'rb'), sheet_name='invest-auto') 
# sharescorefetch(file.STOCK)
lst=['BHARTI AIRTEL', 'PPAP AUTOMOTIVE', 'KANSAI NEROLAC PAINTS', 'MAHINDRA EPC IRRIGATION']
sharescorefetch(lst)