# -*- coding: utf-8 -*-
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options


#options.add_argument("--headless")

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import csv
from multiprocessing import Pool
import threading


threadLocal = threading.local()


def get_driver():
    driver = getattr(threadLocal, 'driver', None)
    if driver is None:
        options = Options()
        options.add_experimental_option("excludeSwitches",
                                        ["ignore-certificate-errors", "safebrowsing-disable-download-protection",
                                         "safebrowsing-disable-auto-update", "disable-client-side-phishing-detection"])

        options.add_argument('--disable-infobars')
        options.add_argument('--disable-extensions')
        options.add_argument('--profile-directory=Default')
        options.add_argument("--incognito")
        options.add_argument("--disable-plugins-discovery")
        prefs = {'profile.default_content_setting_values.automatic_downloads': 1}
        options.add_experimental_option("prefs", prefs)
        #options.add_argument("--headless")
        driver = webdriver.Chrome('chromedriver', options=options)
        setattr(threadLocal, 'driver', driver)
        return driver


def login(zipcode):
    try:
        driver = get_driver()
        driver.get('https://app.dealautomator.com/Account/Account/LogOn')

        time.sleep(2)

        print("enter  Username")
        email = driver.find_element_by_id('Email')
        email.send_keys('jdubwatkins99@gmail.com')

        print("enter  password")
        passwd = driver.find_element_by_id('Password')
        passwd.send_keys('Mikeisnumber1!')

        print("Click  on Signin")
        button = driver.find_element_by_css_selector('button.btn.btn-primary')
        button.click()

        time.sleep(1)

        pass
    except:
        pass

    search_name_get_url(driver,zipcode)

    print("success zipcode:", zipcode ,"\n")
    print("----------------------------------")
    with open("code.txt", "a") as myfile:
        myfile.write(zipcode + "\n")
    driver.close()

def exist(driver):
    try:
        driver.find_element_by_css_selector("div.well.text-center")
    except NoSuchElementException:
        return True
    return False


def exportlead(driver):
    try:
        all = driver.find_element_by_xpath("//*[contains(text(), 'Select All')]")
        driver.execute_script("arguments[0].click();", all)
        time.sleep(2)
        leadbutton = driver.find_element_by_css_selector("button.md-btn.md-btn-primary.btn-block")
        driver.execute_script("arguments[0].click();", leadbutton)
        time.sleep(4)
        buttonarr = driver.find_element_by_class_name("list-actions")
        buttonlist = buttonarr.find_elements_by_css_selector("button.md-btn.md-btn-primary")
        driver.execute_script("arguments[0].click();", buttonlist[0])
        time.sleep(1)
        exportlead = driver.find_element_by_css_selector("a.md-btn.md-btn-primary.md-btn-depressed.float-right")
        exportlead.click()
        time.sleep(6)
        delbutton = driver.find_element_by_css_selector("button.md-btn.md-btn-danger")
        driver.execute_script("arguments[0].click();", delbutton)
        time.sleep(1)
        delete = driver.find_element_by_css_selector("button.md-btn.md-btn-danger.pull-right")
        driver.execute_script("arguments[0].click();", delete)
        time.sleep(2)
        back = driver.find_element_by_css_selector("button.md-btn.btn-default.btn-block")
        driver.execute_script("arguments[0].click();", back)
        time.sleep(1)
    except:
        pass


def download(driver):
    notifys = driver.find_elements_by_class_name("js-notifications-link")
    for id, notify in enumerate(notifys):
        if id == 1:
            driver.execute_script("arguments[0].click();", notify)
            time.sleep(1)
            try:
                simplebar = driver.find_element_by_class_name("simplebar-content")
                contest = simplebar.find_element_by_class_name("list-unstyled")
            
                exports = contest.find_elements_by_tag_name("a")
                for export in exports:
                    driver.execute_script("arguments[0].click();", export)
                    time.sleep(1)
                markasread = driver.find_element_by_css_selector("button.md-btn.md-btn-plain")
                driver.execute_script("arguments[0].click();", markasread)
                time.sleep(1)
            except:
                pass


def search_name_get_url(driver,zipcode):
    try:
        driver.get('https://app.dealautomator.com/Marketing/Leads/Index/Property')
        time.sleep(2)
        ibox = driver.find_element_by_id('search')
        ibox.send_keys(zipcode)
        ibox.send_keys(Keys.ENTER)
        time.sleep(2)

        try:
            find = driver.find_element_by_class_name("addy-item-zip")
            driver.execute_script("arguments[0].click();", find)
            time.sleep(3)

            combo = driver.find_element_by_class_name("ms-choice")
            driver.execute_script("arguments[0].click();", combo)
            time.sleep(1)
            inputlist = driver.find_elements_by_name("selectItem")
            for input in inputlist:
                val = input.get_attribute('value')
                if val == "free & clear":
                    driver.execute_script("arguments[0].click();", input)
                    time.sleep(1)
                    driver.find_element_by_class_name("keep-up").click()
                    time.sleep(1)
                    exitelem = exist(driver)
                    if exitelem == True:
                        exportlead(driver)
                    break
            combo = driver.find_element_by_class_name("ms-choice")
            driver.execute_script("arguments[0].click();", combo)
            inputlist = driver.find_elements_by_name("selectItem")
            for input in inputlist:
                val = input.get_attribute('value')
                if val == "high equity":
                    driver.execute_script("arguments[0].click();", input)
                    time.sleep(1)
                    but = driver.find_element_by_class_name("keep-up")
                    driver.execute_script("arguments[0].click();", but)
                    time.sleep(1)
                    exitelem = exist(driver)
                    if exitelem == True:
                        exportlead(driver)
                    break
            time.sleep(1)
            download(driver)

        except:
            pass
    except Exception as e:
        print(e)
        pass


def main():
    try:

        print("Login Process started")

        try:
            with open("uszips.csv") as f:
                reader = csv.reader(f, delimiter=",")
                arr = []
                for idx, list in enumerate(reader):
                    if idx != 0:
                        if idx % 5 != 0:
                            arr.append(list[0])
                        else:
                            arr.append(list[0])
                            try:
                                # print("getting zipcode for file:",zipcode)
                                with Pool(processes=5) as pool:
                                    pool.map(login, arr)
                                print("------------------------------------")
                            except:
                                pass
                                arr = []
                            arr = []

        except:
            pass

    except Exception as e:
        print(e)
        pass



main()
