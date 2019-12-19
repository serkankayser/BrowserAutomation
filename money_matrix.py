from login import driver
import links
import time


def money_matrix_panel():
    driver.get(links.money_matrix_link)
    time.sleep(10)  # WAIT 10 SECONDS!

    w_pending = driver.find_element_by_class_name(
        'transactionsWorkspacesListItemSpan')
    w_pending.click()
    time.sleep(6)  # WAIT 6 SECONDS!

    drop_down_button = driver.find_element_by_xpath(
        "//span[@class='icon icon-dropdown']")
    drop_down_button.click()
    time.sleep(1)
    reporting5_open = driver.find_element_by_xpath(
        "//li[@class='Product ProductReporting5 ng-scope ng-isolate-scope']")
    reporting5_open.click()
