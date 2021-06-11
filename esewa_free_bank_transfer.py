from chromedriver_py import binary_path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from time import sleep as wait

def typeKeys(input, key:str):
    for letter in key:
        wait(0.01)
        input.send_keys(letter)

def getDriver(profile:str):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument('--disable-blink-features=AutomationControlled') # For ChromeDriver version 79.0.3945.16 or over
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) # For older ChromeDriver under version 79.0.3945.16
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument(f'--user-data-dir=D:\Projects\profile\{profile}')
    driver = webdriver.Chrome(executable_path=binary_path, options=options)
    return driver

# Transfer Bulk Money from Esewa to Bank without Paying a futya kaudi (means: cash)
def BulkEsewaBankTransFer(times:int, phone:str, password:str, accountNumber:str):
    driver = getDriver(phone)
    driver.get("https://www.esewa.com.np")
    waitTill = WebDriverWait(driver, 10)

    for i in range(times):
        # login part
        try:
            wait(2)
            phoneInput = driver.find_element_by_xpath('//*[@id="loginForm"]/div[2]/div[1]/input')
            typeKeys(phoneInput, phone)
            passwordInput = driver.find_element_by_xpath('//*[@id="loginForm"]/div[2]/div[2]/input')
            typeKeys(passwordInput, password)
            wait(3)
            driver.find_element_by_xpath('//*[@id="loginForm"]/div[2]/div[3]/button[1]').click()
        except:
            pass
        
        # Click on Bank Transfer
        waitTill.until(ec.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div[1]/ul/li[5]/a'))).click()

        driver.find_element_by_partial_link_text("Bank Transfer").click()
        wait(2)
        selectBank = driver.find_element_by_xpath('//*[@id="paymentForm"]/div/div/div[1]/div/div/a')
        selectBank.click()
        wait(1)

        bankName = driver.find_element_by_xpath('//*[@id="paymentForm"]/div/div/div[1]/div/div/div/div[1]/input')
        bankName.send_keys("NIC ASIA")
        bankName.send_keys(Keys.RETURN)

        # Choose account number to proceed
        driver.find_element_by_xpath('//*[@id="paymentForm"]/div/div/div[2]/div/div/label[2]').click()
        
        # Type account num
        accountNumberElm = driver.find_element_by_xpath('//*[@id="accountNumber"]')
        print(f'\n\nacc: {accountNumberElm.get_attribute("disabled")} \n\n')
        if accountNumberElm.get_attribute("disabled") != "true":
            typeKeys(accountNumberElm, accountNumber)

        # Acount Holder Name
        accountHolderNameElm = driver.find_element_by_xpath('//*[@id="account_holder_name"]')
        if accountHolderNameElm.get_attribute("disabled") != "true":
            typeKeys(accountHolderNameElm, "Prem Narayan Bhandari")
        # Amount
        typeKeys(driver.find_element_by_xpath('//*[@id="amount"]'), "1000")

        driver.find_element_by_xpath('//*[@id="purpose"]/option[3]').click()

        # Remarks
        typeKeys(driver.find_element_by_xpath('//*[@id="remarks"]'), "Sending to own account: Prem Narayan Bhandari")
        waitTill.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="paymentForm"]/div/div/div[9]/div/button[1]'))).click()
        waitTill.until(ec.visibility_of_element_located((By.XPATH, '/html/body/div[6]/div/div/div/div[3]/div/button[1]'))).click()
        waitTill.until(ec.visibility_of_element_located((By.XPATH, '/html/body/div[4]/div/main/div/div/div[2]/div[2]/section/div/ui-view/div/div/div/div/div[2]/div[2]/div/div[3]/button[1]'))).click()