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
    finished = pyqtSignal()
    
    def __init__(self, text):
        super().__init__()
        
        self.searchText = text[0]
        self.cityText = text[1]
        self.categoryText = text[2]
        self.resultText = text[3]
        
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
            listCompName = self.driver.find_elements(By.CSS_SELECTOR,'c-jobListView__metaItem > i.c-icon--12x12 c-icon--construction + span')
            listContract = self.driver.find_elements(By.CSS_SELECTOR,'c-jobListView__metaItem > i.c-icon--12x12 c-icon--resume + span')
           
            print('yes')
            for w in listWorkName:
                # for c in listCompName:
                #     for con in listContract:
                        result += w.get_attribute("innerHTML") + ',\n'
            
        else:
            result += 'Nothing be Found!'
            
        self.append_info(result)
     
        self.finished.emit()

    def append_info(self, info):
        self.resultText.setText(info)