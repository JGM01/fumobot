from lib2to3.pgen2 import driver
import threading
from typing import final
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
from time import sleep
from datetime import datetime
from fumo import Fumo

# CSS Selectors 
CREDIT_CARD_LABEL = '//label[contains(text(), "Credit card")]'
SHIPPING_METHOD_LABEL = "label[class='form-radio-label'][for='shipping-method19'] span"
WEBSITE = 'https://secure.amiami.com/eng/'
PRODUCT_DETAIL_ADD_CART_8 = '[data-kanshi="productDetailAddCart8"]'
CART_SUBMIT = '[data-kanshi="cartSubmit"]'
CART_MATOME_1_SUBMIT = '[data-kanshi="cartMatome1Submit"]'
CART_MATOME_2_SUBMIT = '[data-kanshi="cartMatome2Submit"]'
CART_MATOME_3_SUBMIT = '[data-kanshi="cartMatome3Submit"]'

ADD_TO_CART_PAGE = 'https://www.amiami.com/eng/cart/'

class FumoPurchaser():
    def __init__(self, fumo, username, password):
        driver_options = Options()
        driver_options.add_argument('--headless')
        self.driver = webdriver.Firefox(options=driver_options)
        #self.driver = webdriver.Firefox()
        self.fumo = fumo
        self.username = username
        self.password = password
        print('[FUMO PURCHASER] Initialized ', end='')
        print(self.fumo.name)

    def run(self):
        try:
            start = datetime.now()
            self.purchase_fumo()
            print('added to cart')
            self.confirm_purchase()
            print('confirmed purchase')
        except Exception as e:
            print(e)
        finally:
            self.driver.quit()
            print(self.fumo.name, end='')
            print(datetime.now()-start)            


    def login(self):
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.NAME, 'email'))).send_keys(self.username)
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.NAME, 'password'))).send_keys(self.password)
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-submit'))).click()
        
    def purchase_fumo(self):
        self.driver.get(self.fumo.value)
        self.idle()
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, PRODUCT_DETAIL_ADD_CART_8))).click()
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, CART_SUBMIT))).click()
        self.login()
    
    def confirm_purchase(self):
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, CART_MATOME_1_SUBMIT))).click()
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, CREDIT_CARD_LABEL))).click()
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, SHIPPING_METHOD_LABEL))).click()
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, CART_MATOME_2_SUBMIT))).click()
        #WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, CART_MATOME_3_SUBMIT))).click()
    
    def idle(self):
        while True:
            try:
                WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, PRODUCT_DETAIL_ADD_CART_8)))
                break
            except TimeoutException:
                self.driver.refresh()
                print(self.fumo.name, end='')
                print(' refreshed')
                continue
