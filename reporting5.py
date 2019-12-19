from login import driver
import links
import time


def reporting5_panel():

    if len(driver.window_handles) > 1:
        driver.switch_to_window(driver.window_handles[1])
    time.sleep(3)

    activity_button = driver.find_element_by_link_text('Activity')
    activity_button.click()

    transactions_button = driver.find_element_by_link_text('Transactions')
    transactions_button.click()

    deposit_click = driver.find_element_by_id('chkTransType_0')
    deposit_click.click()
    time.sleep(1)  # WAIT 1 SECOND!

    withdraw_click = driver.find_element_by_id('chkTransType_1')
    withdraw_click.click()
    time.sleep(1)  # WAIT 1 SECOND!

    vendor2user_click = driver.find_element_by_id('chkTransType_4')
    vendor2user_click.click()
    time.sleep(1)  # WAIT 1 SECOND!

    wallet_debit = driver.find_element_by_id('chkTransType_7')
    wallet_debit.click()
    time.sleep(1)  # WAIT 1 SECOND!

    processing_click = driver.find_element_by_id('cbxTransStatus_1')
    pending_click = driver.find_element_by_id('cbxTransStatus_3')
    processing_click.click()
    pending_click.click()
    time.sleep(1)  # WAIT 1 SECONDS!

    start_day = driver.find_element_by_xpath(
        '/html/body/form/div[3]/table/tbody/tr/td[1]/table/tbody/tr[3]/td[2]/table/tbody/tr/td[2]/input[1]')
    start_day.clear()
    start_day.click()
    start_day.send_keys('13/11/2019')
