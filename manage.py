from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import os
import logging
import sys
from selenium.webdriver.firefox.options import Options
from win32con import SW_HIDE
import win32gui
import os
import pickle

def starter():
 
#   os.environ['WDM_PROGRESS_BAR'] = str(0)
#   os.environ['WDM_LOCAL'] = '1'
#   os.environ['WDM_SSL_VERIFY'] = '0'
  # user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0'
  # option = webdriver.FirefoxOptions()
  # option.headless = True
  # option.add_argument(f'user-agent={user_agent}')
  # option.add_argument('--ignore-certificate-errors')
  # option.add_argument('--allow-running-insecure-content')
  # option.add_argument('--disable-extensions')
  # option.add_argument('--start-maximized')
  # option.add_argument('--disable-gpu')
  # option.add_argument('--disable-dev-shm-usage')
  # option.add_argument('--no-sandbox')
  
  sys.stdout.reconfigure(encoding='utf-8')
  os.environ['GH_TOKEN'] = "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"
  #webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
  os.environ['WDM_LOG'] = str(logging.NOTSET)


def signin():
  signdIn = False
  
  # options = Options()
  # options.add_argument('--headless')
  driverClass = WebDriverSingleton()
  driver = driverClass.get_driver()
  
  # user_cookie = driver.get_cookie("user")
  # password_cookie = driver.get_cookie("password")
  
  if os.path.exists('cookies.pkl'):
    signdIn = True
  
  # print(directory)
  # if os.path.isdir(directory):
  #   signdIn = True
  # print(signdIn)
  print(signdIn)
  return signdIn

class WebDriverSingleton:
    _instance = None

    def __new__(cls, option=None):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.driver = webdriver.Firefox(options=option)
        return cls._instance

    def get_driver(self):
        return self.driver
    


  
  
  

  
  
  
  

