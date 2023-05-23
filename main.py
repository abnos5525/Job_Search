import manage
import os
from colorama import Fore
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import uic
from PyQt5.QtCore import QThread
from manage import WebDriverSingleton
from Search import Search
from SignIn import SignIn
<<<<<<< HEAD
from PyQt5.QtCore import pyqtSignal
=======


>>>>>>> 7f4f34bbfd1e5737eb2a9375c0fb1f8f95ccd43e
class Window(QMainWindow):
    threads_finished = pyqtSignal()
    def __init__(self):
        super().__init__()
        uic.loadUi("view.ui",self)
        self.stackedWidget.setCurrentIndex(0)
        self.txtResult.setLayoutDirection(Qt.RightToLeft)
        #--------------------------------------------------
        
        if manage.signin() == False:
            self.btnExit.setEnabled(False)
            self.btnExit.setStyleSheet("background-color: #f0f0f0;")
            self.btnSearch.setText("ورود")
            self.txtJob.setEnabled(False)
        else:
            self.btnExit.setEnabled(True)
            self.txtUsername.setEnabled(False)
            self.txtPassword.setEnabled(False)
            self.btnSearch.setText("جستجو")
            
        # Declarations
        self.first_thread = None
        self.second_thread = None
        self.threads_finished = False
        
        
        #Actions
        #--------------------------------------------------
        self.btnResult.clicked.connect(self.resultPage)
        self.btnHome.clicked.connect(self.resultPage)
        self.btnSearch.clicked.connect(self.result)
        self.btnExit.clicked.connect(self.exitLog)
        
        self.btnExit.clicked.connect(self.cleanupThreads) 
        #--------------------------------------------------
        
    #switch to pages
    def resultPage(self):
        if self.stackedWidget.currentIndex() == 0:
            self.stackedWidget.setCurrentIndex(1)
        else:
            self.stackedWidget.setCurrentIndex(0)
            
    def result(self):
        
        jobText = self.txtJob.text()
        cityText = self.cmCity.currentText()
        categoryText = self.cmCategory.currentText()
        
        username = self.txtUsername.text()
        password = self.txtPassword.text()

        if username != '' and  password != '':
            self.txtResult.clear()
            self.btnSearch.setEnabled(False)
            self.btnSearch.setStyleSheet("background-color: #f0f0f0;")
            self.signInInfo = [username,password]
            self.searchInfo = None
            
            if not manage.signin():
                try:
                    if self.first_thread is None or not self.first_thread.isRunning():
                        self.cleanupThreads() 
                        self.first_thread = QThread()
                        self.first_worker = SignIn(self.signInInfo)
                        self.first_worker.moveToThread(self.first_thread)
                        self.first_worker.finished.connect(self.update_result)
                        self.first_worker.finished.connect(self.start_second_worker)
                        self.first_worker.finished.connect(self.first_thread.quit)
                        self.first_worker.finished.connect(self.first_worker.deleteLater)
                        self.first_thread.finished.connect(self.first_thread.deleteLater)
                        
                        self.first_worker.finished.connect(self.handleFirstWorkerFinished)
                        self.first_worker.finished.connect(self.start_second_worker)
                        self.first_thread.started.connect(self.first_worker.do_work)
                        self.first_thread.start()
                    
                except Exception as e:
                    print(e)
            else:
                if self.second_thread is None or not self.second_thread.isRunning() and self.searchInfo != '':
                    self.searchInfo = [jobText,cityText,categoryText]
                    self.second_thread = QThread()
                    self.second_worker = Search(self.searchInfo)
                    self.second_worker.moveToThread(self.second_thread)
                    self.second_worker.finished.connect(self.update_result)
                    self.second_worker.finished.connect(self.second_thread.quit)
                    self.second_worker.finished.connect(self.second_worker.deleteLater)
                    self.second_thread.finished.connect(self.second_thread.deleteLater)
                    
                    self.second_worker.finished.connect(self.handleSecondWorkerFinished)
                    self.second_thread.started.connect(self.second_worker.do_work)
                    self.second_thread.start()
                    
                else:
                    QMessageBox.warning(self,'اخطار','فیلدها را پر کنید')
            
            
            
        else:
            QMessageBox.warning(self,'اخطار','فیلدها را پر کنید')
            
    def handleFirstWorkerFinished(self):
        self.cleanupThreads()

    def handleSecondWorkerFinished(self):
        self.cleanupThreads()
            
    def update_result(self, result):
        self.thResult = result
        self.txtResult.setText(result)
        if os.path.exists('cookies.pkl'):
            self.btnExit.setEnabled(True)
            self.btnExit.setStyleSheet("background-color: red;color:white;")
            self.btnSearch.setText("جستجو")
            self.txtJob.setEnabled(True)
        self.btnSearch.setEnabled(True)
        self.btnSearch.setStyleSheet("background-color: green;color:white;")
        
    def cleanupThreads(self):
        # Clean up threads
        if self.first_thread is not None:
            self.first_thread.quit()
            self.first_thread.wait()
            self.first_thread = None
        if self.second_thread is not None:
            self.second_thread.quit()
            self.second_thread.wait()
            self.second_thread = None
        
        
        
            
    # def start(self):
    #     if manage.signin() == False:
    #         if not self.first_thread.isRunning():
    #         #self.first_thread.started.connect(self.first_worker.do_work)
    #             self.first_thread.start()

    def start_second_worker(self):
        if self.thResult is None:
            self.first_worker.finished.disconnect(self.start_second_worker)
            self.second_thread.started.connect(self.second_worker.do_work)
            self.second_thread.start()
            
    def exitLog(self):
        self.driverClass = WebDriverSingleton()
        self.driver = self.driverClass.get_driver()
        self.driver.delete_all_cookies()
        if os.path.exists('cookies.pkl'):
            os.remove('cookies.pkl')
        self.btnExit.setEnabled(False)
        self.btnExit.setStyleSheet("background-color: #f0f0f0;")
        self.txtUsername.setEnabled(True)
        self.txtPassword.setEnabled(True)
        self.txtUsername.clear()
        self.txtPassword.clear()
        self.btnSearch.setText("ورود")
        self.txtJob.setEnabled(False)
        
        self.cleanupThreads()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
