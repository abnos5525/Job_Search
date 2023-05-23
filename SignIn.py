import manage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, QObject
from selenium.webdriver.firefox.options import Options
import os

from manage import WebDriverSingleton
import pickle

class SignIn(QObject):
    finished = pyqtSignal(str)
    
    def __init__(self, text):
        super().__init__()
        self.username = text[0]
        self.password = text[1]
        
    def do_work(self):
        # options.headless = True
        
            # self.current_directory = os.path.dirname(os.path.abspath(__file__))
            # self.directory = self.current_directory + '\history'
            # print(self.directory)
            # os.mkdir(self.directory)

            # self.options = Options()
            # self.options.add_argument(f"--profile={self.directory}")
            #self.options.add_argument(self.directory)
        try:
            options = Options()
            options.add_argument('--headless=False')
            
            self.driverClass = WebDriverSingleton(option=options)
            self.driver = self.driverClass.get_driver()

            self.driver.get('https://jobinja.ir/')
            signin = WebDriverWait(self.driver,4).until(ec.presence_of_element_located((By.XPATH , '/html/body/div/header/div[1]/div/div[2]/div[2]/div[1]/a[1]')))
            signin.click()
            time.sleep(3)
            self.driver.find_element(By.XPATH, '//*[@id="identifier"]').send_keys(self.username)
            self.driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(self.password)
            time.sleep(1)
            self.driver.find_element(By.XPATH, '/html/body/div/div/div[1]/form/div[2]/div/input[4]').click()
            expected_url = 'https://jobinja.ir/login/user'
            result = ' '
            if self.driver.current_url == expected_url:
                result = 'Email or password is incorrect!'
            else:
            
                self.driver.add_cookie({"name": "user", "value": self.username})
                self.driver.add_cookie({"name": "password", "value": self.password})
                cookies_file = 'cookies.pkl'
                cookies = self.driver.get_cookies()
                with open(cookies_file, 'wb') as file:
                    pickle.dump(cookies, file)
                    
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
            
            self.finished.emit(result)
            self.deleteLater()
            
        except Exception as e:
            print(e)
        #------------------------------------------------