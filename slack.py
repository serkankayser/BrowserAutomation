from login import driver
from selenium.webdriver.common.keys import Keys
import credentials
import time


def slack_panel():
    driver.execute_script("window.open('https://jojack.slack.com/');")
    driver.switch_to_window(driver.window_handles[2])  # SHOW SLACK
    time.sleep(7)  # WAIT 7 SECONDS!

    mail = driver.find_element_by_css_selector('input[type="email"]')
    mail.send_keys(credentials.slack_mail)
    time.sleep(3)
    ps = driver.find_element_by_css_selector('input[type="password"]')
    ps.send_keys(credentials.slack_pass)

    submit_button = driver.find_element_by_xpath(
        '/html/body/div[1]/div[1]/div[2]/div/form/p[5]/button')
    submit_button.click()
    time.sleep(1)
    jump_to = driver.find_element_by_xpath(
        "/html/body/div[2]/div/div/div[3]/div/nav/div[1]/button")
    jump_to.click()
    search_for_channel = driver.find_element_by_xpath(
        "/html/body/div[6]/div/div/div/div[1]/div/div/div[1]/p")
    search_for_channel.send_keys("Cengiz")
    time.sleep(1)
    search_for_channel.send_keys(Keys.ENTER)
    time.sleep(5)

    driver.switch_to_window(driver.window_handles[0])  # SHOW THE MM PANEL
