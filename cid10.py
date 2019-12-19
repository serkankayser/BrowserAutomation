from login import driver
from slack import slack_panel
from selenium.webdriver.common.keys import Keys
import time
cek_ok = "Cekim onay"
cek_decline = "TL degerinde en az 1.30 oranlı bahis almanız veya belirtilen miktarda casino alanında oyun oynamanız gerekmektedir."
filtered_time_withdraw = []
filtered_cid = []
filtered_trans_type = []
filtered_last_note = []
amount = []
filtered_number_row = []
filtered_current_page = []
items = []
last_kt = []


def get10_cid():
    for i in range(1, 31):
        customer_id = driver.find_elements_by_xpath(
            f"/html/body/div/div/div[2]/div/div/div/div/div/ui-view/div/div/div[2]/div/ubo-tma-table/div/div[2]/table/tbody/tr[{i}]/td[2]/span")
        filtered_cid.append(customer_id[0].text[5:])
    get_time()


def get_time():
    for i in range(1, 31):
        time_withdraw = driver.find_elements_by_xpath(
            f"/html/body/div/div/div[2]/div/div/div/div/div/ui-view/div/div/div[2]/div/ubo-tma-table/div/div[2]/table/tbody/tr[{i}]/td[1]/span[2]")
        filtered_time_withdraw.append(time_withdraw[0].text)

    last_kt.append(filtered_time_withdraw[0])
    if len(last_kt) > 1:
        if last_kt[0] in filtered_time_withdraw:
            index_last_kt = filtered_time_withdraw.index(last_kt[0])
            del filtered_time_withdraw[index_last_kt:]
            del filtered_cid[index_last_kt:]
            del last_kt[0]
        else:
            driver.switch_to_window(driver.window_handles[2])
            send_message = driver.find_element_by_xpath(
                "/html/body/div[2]/div/div/div[4]/div/div/footer/div/div/div[1]/div/div[1]")
            send_message.send_keys("NU EXISTA DEPOSIT. CONTROLEAZA MANUAL!")
            send_message.send_keys(Keys.ENTER)
            driver.switch_to_window(driver.window_handles[0])
            del last_kt[0]
    cp10_cid()


def cp10_cid():
    if len(filtered_cid) > 0:
        time.sleep(2)   # WAIT 2 SECONDS!
        # SHOW THE REPORTING5 PANEL
        driver.switch_to_window(driver.window_handles[1])

        userid_box = driver.find_element_by_name(
            'txtUserID')       # Reporting5
        # Reporting5
        userid_box.clear()
        userid_box.send_keys(filtered_cid[-1])

        show_report = driver.find_element_by_name(
            'btnShowReport')  # Reporting5
        show_report.click()

        time.sleep(2)
        get_data_from_r5()

    else:
        refresh_button = driver.find_element_by_xpath(
            "/html/body/div/div/div[2]/div/div/div/div/div/ui-view/div/div/div[2]/div/section/div[3]/button[1]")
        refresh_button.click()
        time.sleep(10)   # WAIT 10 SECONDS!
        get10_cid()


def get_data_from_r5():
    counter_withdraw = 0
    for row in range(2, 53):
        number_row = driver.find_element_by_xpath(
            f"/html/body/form/div[3]/div[4]/table/tbody/tr[{row}]/td[2]")
        filtered_number_row.append(number_row.text)
        if len(filtered_number_row[-1]) != 9:
            break
    for i in range(2, row):
        trans_type = driver.find_element_by_xpath(
            f"/html/body/form/div[3]/div[4]/table/tbody/tr[{i}]/td[20]")
        filtered_trans_type.append(trans_type.text)

        debit_amount = driver.find_element_by_xpath(
            f"/html/body/form/div[3]/div[4]/table/tbody/tr[{i}]/td[13]")
        amount.append(debit_amount.text)

        last_note = driver.find_element_by_xpath(
            f"/html/body/form/div[3]/div[4]/table/tbody/tr[{i}]/td[25]")
        filtered_last_note.append(last_note.text[0:2].lower())

        if len(amount[-1]) > 7:
            amount[-1] = amount[-1].replace(',', '')
        balance = float(amount[-1])

        if filtered_trans_type[-1] == "Deposit" or filtered_trans_type[-1] == "Vendor2User":
            if filtered_trans_type[-1] == "Vendor2User" and balance == 0.00:
                continue
            break

        if filtered_last_note[-1] == "gh":
            break

        if filtered_trans_type[-1] == "Withdraw" and balance >= 5.00:
            counter_withdraw += 1
    find_deposit(filtered_trans_type, amount, balance, counter_withdraw)


def approve_withdraw():
    driver.switch_to_window(driver.window_handles[2])
    send_message = driver.find_element_by_xpath(
        "/html/body/div[2]/div/div/div[4]/div/div/footer/div/div/div[1]/div/div[1]")
    send_message.send_keys(
        filtered_time_withdraw[-1], " ", filtered_cid[-1], " - ", cek_ok)
    send_message.send_keys(Keys.ENTER)
    amount.clear()
    filtered_trans_type.clear()
    filtered_last_note.clear()
    filtered_number_row.clear()
    del filtered_cid[-1]
    del filtered_time_withdraw[-1]
    driver.switch_to_window(driver.window_handles[0])
    cp10_cid()


def decline_withdraw(balance):
    balance = str(balance)
    driver.switch_to_window(driver.window_handles[2])
    send_message = driver.find_element_by_xpath(
        "/html/body/div[2]/div/div/div[4]/div/div/footer/div/div/div[1]/div/div[1]")
    send_message.send_keys(
        filtered_time_withdraw[-1], " ", filtered_cid[-1], " - ", balance, " ", cek_decline)
    send_message.send_keys(Keys.ENTER)
    amount.clear()
    filtered_trans_type.clear()
    filtered_last_note.clear()
    filtered_number_row.clear()
    del filtered_cid[-1]
    del filtered_time_withdraw[-1]
    driver.switch_to_window(driver.window_handles[0])
    cp10_cid()


def find_deposit(filtered_trans_type, amount, balance, counter_withdraw):
    if filtered_last_note[-1] == "gh":
        print("gh eklemesi var.")
        approve_withdraw()

    elif filtered_trans_type[-1] == "Deposit" or filtered_trans_type[-1] == "Vendor2User":
        for i in range(len(filtered_trans_type)-1, 0, -1):
            if filtered_trans_type[i-1] == "WalletDebit":
                balance -= float(amount[i-1])
                del amount[-1]
                del filtered_trans_type[-1]
                if balance <= 0:
                    approve_withdraw()
                    break
                if i == 1:
                    decline_withdraw(balance)
                    break

            elif i == 1 and filtered_trans_type[i-1] == "Withdraw":
                decline_withdraw(balance)
                break

            elif 'WalletDebit' not in filtered_trans_type:
                driver.switch_to_window(driver.window_handles[2])
                send_message = driver.find_element_by_xpath(
                    "/html/body/div[2]/div/div/div[4]/div/div/footer/div/div/div[1]/div/div[1]")
                send_message.send_keys(
                    filtered_time_withdraw[-1], " ", filtered_cid[-1], " - ", amount[-1], " ", cek_decline)
                send_message.send_keys(Keys.ENTER)
                amount.clear()
                filtered_trans_type.clear()
                filtered_last_note.clear()
                filtered_number_row.clear()
                del filtered_cid[-1]
                del filtered_time_withdraw[-1]
                driver.switch_to_window(driver.window_handles[0])
                cp10_cid()
                break

    elif counter_withdraw >= 2:                  # If we have 2 withdraws in list -> approve withdraw
        print("2 cekimi var...")
        approve_withdraw()

    elif filtered_trans_type[-1] != "Deposit" or filtered_trans_type[-1] != "Vendor2User":
        driver.execute_script("window.scrollTo(0, 3000)")
        time.sleep(5)

        current_page = driver.find_element_by_xpath(
            f"/html/body/form/div[3]/div[5]/span")
        filtered_current_page.append(current_page.text)

        span = driver.find_element_by_xpath(
            f"/html/body/form/div[3]/div[5]/a[{int(filtered_current_page[-1])+2}]")
        if int(filtered_current_page[-1]) > 5:
            approve_withdraw()
        # if int(filtered_current_page[-1]) >= 11 and int(filtered_current_page[-1]) < 21:
        #     span = driver.find_element_by_xpath(
        #         f"/html/body/form/div[3]/div[5]/a[{int(filtered_current_page[-1])-7}]")
        # elif int(filtered_current_page[-1]) >= 21 and int(filtered_current_page[-1]) < 31:
        #     span = driver.find_element_by_xpath(
        #         f"/html/body/form/div[3]/div[5]/a[{int(filtered_current_page[-1])-17}]")

        span.click()
        filtered_number_row.clear()
        filtered_current_page.clear()
        get_data_from_r5()
