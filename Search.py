from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import os
from colorama import Fore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, QObject
from selenium.webdriver.firefox.options import Options
import SignIn
from manage import WebDriverSingleton
import pickle

class Search(QObject):
    finished = pyqtSignal(str)
    
    def __init__(self, text):
        super().__init__()
        
        self.searchText = text[0]
        self.cityText = text[1]
        self.categoryText = text[2]
        
    def do_work(self):
        #options = Options()
        # options.headless = True
        #driver = webdriver.Firefox()
        self.driverClass = WebDriverSingleton()
        self.driver = self.driverClass.get_driver()
        
        cookies_file = 'cookies.pkl'
        #cookies = self.driver.get_cookies()
        with open(cookies_file, 'rb') as file:
            cookies  = pickle.load(file)
        
        
        self.driver.get('https://jobinja.ir/')
        
        for cookie in cookies:
            self.driver.add_cookie(cookie)
            
        self.driver.refresh()
        
        result = ""
        #search = WebDriverWait(self.driver,5).until(ec.presence_of_element_located((By.XPATH , '/html/body/div/div[2]/div/form/div[1]/input')))
        time.sleep(4)
        search = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/div/form/div[1]/input')
        search.send_keys(self.searchText)
        time.sleep(1)
        
        self.driver.find_element(By.XPATH, '/html/body/div/div[2]/div/form/div[2]/span').click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, '/html/body/span/span/span[1]/input').send_keys(self.cityText, Keys.ENTER)
        
        time.sleep(1)
        
        self.driver.find_element(By.XPATH, '/html/body/div/div[2]/div/form/div[3]/span').click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, '/html/body/span/span/span[1]/input').send_keys(self.categoryText, Keys.ENTER)
        
        self.driver.find_element(By.XPATH, '/html/body/div/div[2]/div/form/div[4]').click()
        time.sleep(3)
        
        window = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/form[2]/div/div/div[2]/section/div/ul')
        ulTag = window.find_element(By.CLASS_NAME, 'o-listView__item')
        
        if ulTag:
            listWorkName = self.driver.find_elements(By.CLASS_NAME,'c-jobListView__titleLink')
            cityName = self.driver.find_elements(By.CSS_SELECTOR,'i.c-icon--place + span')
            listCompName = self.driver.find_elements(By.CSS_SELECTOR,'i.c-icon--construction + span')
            listContract1 = self.driver.find_elements(By.CSS_SELECTOR,'c-jobListView__metaItem > span:first-child')
            listContract2 = self.driver.find_elements(By.CSS_SELECTOR,'c-jobListView__metaItem > span:nth-child(2)')
           
            for w,city,c in zip(listWorkName,cityName,listCompName):
                    # for c1 in listCompName:
                    #     for c2 in listContract1:
                    #         for con in listContract2:
                                text = w.get_attribute("innerHTML")
                                result += text.lstrip() + '\n'
                                text = city.get_attribute("innerHTML")
                                result += text.lstrip() + '\n'
                                text = c.get_attribute("innerHTML")
                                result += text.lstrip() + '\n'
                                # text = con1.get_attribute("innerHTML")
                                # result += text.lstrip() + '\n'
                                # text = con2.get_attribute("innerHTML")
                                # result += text.lstrip() + '\n'
                                result += '----------------\n'
            
        else:
            result += 'Nothing be Found!'
            
        # self.append_info(result)
     
        self.finished.emit(result)

    # def append_info(self, info):
    #     self.resultText.setText(info)