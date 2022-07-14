base_link = "https://www.meb.gov.tr/sinavlar/sonuc/sorgu.php?SINAV_ID="
sinav_id = "24DBA251CB781CFEADB04A5C53BB878A"
site_link = base_link+sinav_id
from lib2to3.pgen2 import driver
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from PyQt5.QtGui import QPixmap
import base64


def loopThrough(win, browser, iterr, df: pd.DataFrame):
    try:
        idx, row = next(iterr)
    except StopIteration:
        win.surnameLabel.setText("Finish")
        idx = -1
        row = df.loc(1)
    
    if idx == -1:
        return idx
    
    browser.get(site_link)
    
    win.nameLabel.setText(row["Ad Soyad"])
    win.countLabel.setText(str(idx + 1)+"/"+str(len(df.index)))
    dogum_tarihi = row["Doğum Tarihi"]
    win.surnameLabel.setText(dogum_tarihi)

    tcno = browser.find_element(by=By.CSS_SELECTOR, value="#ADAY_NO")
    tcno.send_keys(row['TC Kimlik'])

    gun = Select(browser.find_element(by=By.CSS_SELECTOR, value="#GUN"))
    ay = Select(browser.find_element(by=By.CSS_SELECTOR, value="#AY"))
    yil = Select(browser.find_element(by=By.CSS_SELECTOR, value="#YIL"))

    gun.select_by_value(dogum_tarihi[0:2])
    ay.select_by_value(dogum_tarihi[3:5])
    yil.select_by_value(dogum_tarihi[6:10])

    captcha_resim = browser.find_element(by=By.CSS_SELECTOR, value="#capcha")
    
    pic = QPixmap()
    pic.loadFromData(base64.b64decode(captcha_resim.screenshot_as_base64))
    win.captchaView.setPixmap(pic)
    return idx

def getYuzdelik(win, browser: webdriver.Chrome, idx, df: pd.DataFrame):
    yuzdelik_selector = "div.center:nth-child(3) > table:nth-child(3) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2)"
    try:
        element = WebDriverWait(browser, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, yuzdelik_selector))
            )
        df.at[idx, "Yüzdeliği"] =  element.text
    except TimeoutException:
        try:
            element = browser.find_element(By.CSS_SELECTOR, "#hata")
            if (element.text[0:3] == "T.C"):
                df.at[idx, "Yüzdeliği"] = "TC No Hatali"
            else:
                df.at[idx, "Yüzdeliği"] = "Güvenlik Kodu Hatali"
        except NoSuchElementException:
            df.at[idx, "Yüzdeliği"] = "Bilinmeyen Hata"
    finally:
        df.to_csv(path_or_buf="new_data.csv")
        df.to_excel(excel_writer="new_data.xlsx")
