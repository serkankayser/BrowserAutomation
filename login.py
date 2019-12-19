from selenium import webdriver
import credentials
import links
import time

driver = webdriver.Chrome()
driver.fullscreen_window()
driver.get(links.login_link)
username_box = driver.find_element_by_css_selector('input')
username_box.send_keys(credentials.e_mail)
password_box = driver.find_element_by_css_selector('input[type="password"]')
password_box.send_keys(credentials.password)
password_box.submit()
time.sleep(5)           # WAIT 5 SECONDS AFTER LOGIN!
