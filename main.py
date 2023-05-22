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

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("view.ui",self)
        self.stackedWidget.setCurrentIndex(0)
        self.txtResult.setLayoutDirection(Qt.RightToLeft)
        #--------------------------------------------------
        
        if manage.signin() == False:
            self.btnExit.setEnabled(False)
            self.btnExit.setStyleSheet("background-color: #f0f0f0;")
        else:
            self.btnExit.setEnabled(True)
        
        
        #Actions
        #--------------------------------------------------
        self.btnResult.clicked.connect(self.resultPage)
        self.btnHome.clicked.connect(self.resultPage)
        self.btnSearch.clicked.connect(self.result)
        self.btnExit.clicked.connect(self.exitLog)
        #--------------------------------------------------
        
    #switch to pages
    def resultPage(self):
        if self.stackedWidget.currentIndex() == 0:
            self.stackedWidget.setCurrentIndex(1)
        else:
            self.stackedWidget.setCurrentIndex(0)
            
    def result(self):
        self.txtResult.clear()
        jobText = self.txtJob.text()
        cityText = self.cmCity.currentText()
        categoryText = self.cmCategory.currentText()
        
        username = self.txtUsername.text()
        password = self.txtPassword.text()
        
        resultText = self.txtResult.toPlainText()
        if jobText != '' or username != '' or  password != '':
            self.signInInfo = [username,password]
            self.searchInfo = [jobText,cityText,categoryText]
            
            
            if not manage.signin():
                self.first_thread = QThread()
                self.first_worker = SignIn(self.signInInfo)
                self.first_worker.moveToThread(self.first_thread)

                self.second_thread = QThread()
                self.second_worker = Search(self.searchInfo)
                self.second_worker.moveToThread(self.second_thread)

                self.first_worker.finished.connect(self.start_second_worker)
                self.second_worker.finished.connect(self.second_thread.quit)
                self.second_worker.finished.connect(self.second_worker.deleteLater)
                self.second_thread.finished.connect(self.second_thread.deleteLater)

                self.second_worker.finished.connect(self.update_result)

                self.first_thread.started.connect(self.first_worker.do_work)
                self.first_thread.start()

            else:  
                self.second_thread = QThread()
                self.second_worker = Search(self.searchInfo)
                self.second_worker.moveToThread(self.second_thread)

                self.second_worker.finished.connect(self.second_thread.quit)
                self.second_worker.finished.connect(self.second_worker.deleteLater)
                self.second_thread.finished.connect(self.second_thread.deleteLater)
                
                self.second_worker.finished.connect(self.update_result)

                self.second_thread.started.connect(self.second_worker.do_work)
                self.second_thread.start()
            
            
            
        else:
            QMessageBox.warning(self,'اخطار','فیلدها را پر کنید')
            
    def update_result(self, result):
        self.txtResult.setText(result)
            
    def start(self):
        if manage.signin() == False:
            self.first_thread.started.connect(self.first_worker.do_work)
            self.first_thread.start()

    def start_second_worker(self):
        self.first_worker.finished.disconnect(self.start_second_worker)
        self.second_thread.started.connect(self.second_worker.do_work)
        self.second_thread.start()
            
    def exitLog(self):
        # current_directory = os.path.dirname(os.path.abspath(__file__))
        # directory = current_directory + '\history'
        # print(directory)
        # shutil.rmtree(directory)
        self.driverClass = WebDriverSingleton()
        self.driver = self.driverClass.get_driver()
        self.driver.delete_all_cookies()
        if os.path.exists('cookies.pkl'):
            os.remove('cookies.pkl')
        self.btnExit.setEnabled(False)
        self.btnExit.setStyleSheet("background-color: #f0f0f0;")
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())