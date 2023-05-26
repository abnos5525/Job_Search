from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import os
import logging
import sys
from selenium.webdriver.firefox.options import Options
from win32con import SW_HIDE
import os

def starter():
  
  sys.stdout.reconfigure(encoding='utf-8')
  os.environ['GH_TOKEN'] = "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"
  webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
  os.environ['WDM_LOG'] = str(logging.NOTSET)


def signin():
  signdIn = False
  
  options = Options()
  options.add_argument('--headless')
  driverClass = WebDriverSingleton(option=options)
  driverClass.get_driver()

  
  if os.path.exists('cookies.pkl'):
    signdIn = True

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
    


  
  
  

  
  
  
  

