from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from colorama import Fore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, QObject
from manage import WebDriverSingleton
import pickle

class Search(QObject):
    finished = pyqtSignal(str,str)
    
    def __init__(self, text):
        super().__init__()
        
        self.searchText = text[0]
        self.cityText = text[1]
        self.categoryText = text[2]
        
    def do_work(self):
        self.driverClass = WebDriverSingleton()
        self.driver = self.driverClass.get_driver()
        
        cookies_file = 'cookies.pkl'
        with open(cookies_file, 'rb') as file:
            cookies  = pickle.load(file)
        
        
        self.driver.get('https://jobinja.ir/')
        
        for cookie in cookies:
            self.driver.add_cookie(cookie)
            
        self.driver.refresh()
        
        result = ""
        time.sleep(2)
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
        print('yeeeeees1')
        self.driver.find_element(By.XPATH, '/html/body/div/div[2]/div/form/div[4]').click()
        message = ''
        time.sleep(3)
        try:
            window = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/form[2]/div/div/div[2]/section/div/ul')
            ulTag = window.find_element(By.CLASS_NAME, 'o-listView__item')
            print('yeeeeees2')
            
            
            if ulTag:
                listWorkName = self.driver.find_elements(By.CLASS_NAME,'c-jobListView__titleLink')
                cityName = self.driver.find_elements(By.CSS_SELECTOR,'i.c-icon--place + span')
                listCompName = self.driver.find_elements(By.CSS_SELECTOR,'i.c-icon--construction + span')
                listContract1 = self.driver.find_elements(By.CSS_SELECTOR,'c-jobListView__metaItem > span:first-child')
                listContract2 = self.driver.find_elements(By.CSS_SELECTOR,'c-jobListView__metaItem > span:nth-child(2)')
                print('yeeeeees3')
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
                message = 'چند مورد یافت شد!'
        except Exception as e:
            message = 'چیزی یافت نشد!'
            

        self.finished.emit(result,message)