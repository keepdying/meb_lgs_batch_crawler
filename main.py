import sys
import requests as req
import pandas as pd
import base64
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from main_window_ui import Ui_MainWindow
from events import *

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self, browser, iterr, df)

chrome_options = Options()
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument("--headless")
base_link = "https://www.meb.gov.tr/sinavlar/sonuc/sorgu.php?SINAV_ID="
sinav_id = "24DBA251CB781CFEADB04A5C53BB878A"
site_link = base_link+sinav_id
# browser = webdriver.Chrome(options=chrome_options)

if __name__ == "__main__":
    browser = webdriver.Chrome(options= chrome_options)
    app = QApplication(sys.argv)
    df = pd.read_csv('data.csv',header= 1)
    iterr = df.iterrows()
    win = Window()
    win.show()
    loopThrough(win, browser, iterr, df)
    sys.exit(app.exec())