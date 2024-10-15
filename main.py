from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import smtplib

# Import the email modules we'll need
from email.message import EmailMessage

import time

def send_email():
    msg = EmailMessage()
    msg.set_content("Study Abroad application open\ntime: "+time.ctime())
    email_from = ""
    email_to = ""
    password = ""
    with open("secrets.txt","r") as f:
        email_from = f.readline()
        email_to = f.readline()
        password = f.readline()
    msg['Subject'] = "Study Abroad Application Open"
    msg['From'] = email_from
    msg['To'] = email_to

    s = smtplib.SMTP('smtp.gmail.com',587)
    s.ehlo()

    s.starttls()
    
    s.login(email_from, password)
    s.send_message(msg)
    s.quit()

def main():
    interval = 60
    driver = webdriver.Chrome()
    driver.get("https://utdallas-ea.terradotta.com/_portal/tds-program-brochure?programid=10459")

    while True:
        try:
            element = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.ID, "mat-tab-label-0-1"))
                )
            element.click()
        except Exception:
            send_email()
            print("failed to load "+time.ctime())
            time.sleep(interval)
            driver.refresh()
            continue

        try:
            WebDriverWait(driver, 15).until(
                    EC.text_to_be_present_in_element((By.TAG_NAME, "i"),"application")
                )
            elem = driver.find_element(By.TAG_NAME,"i")
            print(elem.text)
            text = elem.text

            if(text != "There are currently no active application cycles for this program."):
                print("open: "+time.ctime())
                send_email()
            else:
                print("not open: "+time.ctime())
            time.sleep(interval)
        except Exception:
            send_email()
            print("failed to load "+time.ctime())
            time.sleep(interval)
        driver.refresh()

        


if __name__=="__main__":
    main()