from tabnanny import check
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
from datetime import datetime

# CSS Selectors 
CREDIT_CARD_LABEL = '//label[contains(text(), "Credit card")]'
SHIPPING_METHOD_LABEL = "label[class='form-radio-label'][for='shipping-method19'] span"
WEBSITE = 'https://secure.amiami.com/eng/'
PRODUCT_DETAIL_ADD_CART_8 = '[data-kanshi="productDetailAddCart8"]'
CART_SUBMIT = '[data-kanshi="cartSubmit"]'
CART_MATOME_1_SUBMIT = '[data-kanshi="cartMatome1Submit"]'
CART_MATOME_2_SUBMIT = '[data-kanshi="cartMatome2Submit"]'
CART_MATOME_3_SUBMIT = '[data-kanshi="cartMatome3Submit"]'

PROCEED_TO_CHECKOUT_PAGE = 'https://secure.amiami.com/eng/cartmatome/1/'

class FumoPurchaser():
    def __init__(self, fumo, username, password):
        #driver_options = Options()
        #driver_options.add_argument('--headless')
        #self.driver = webdriver.Firefox(options=driver_options)
        #self.driver = webdriver.Firefox()
        self.fumo = fumo
        self.username = username
        self.password = password
        print('[FUMO PURCHASER] Initialized ', end='')
        print(self.fumo.name)

    def run(self):

        done = False
        while(not done):
            try:
                driver_options = Options()
                driver_options.add_argument('--headless')
                self.driver = webdriver.Firefox(options=driver_options)
                self.purchase_fumo()
                self.login()
                self.check_for_error()
                self.confirm_purchase()
            except Exception as e:
                self.driver.quit()
                self.debug(self.driver.current_url, ' bugged out')
                #print(e)
                self.run()
            finally:
                #self.driver.quit()
                print(self.fumo.name, end='')
                print(' exited')
                done = True


    def login(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.NAME, 'email'))).send_keys(self.username)
        self.debug(self.driver.current_url, 'input email')
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.NAME, 'password'))).send_keys(self.password)
        self.debug(self.driver.current_url, 'input password')
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-submit'))).click()
        self.debug(self.driver.current_url, 'clicked log-in')
        
    def purchase_fumo(self):
        while(True):
            try:
                self.driver.get(self.fumo.value)
                break
            except:
                print(self.fumo.name, end='')
                print(' could not reach product page, retrying')
                self.driver.get(self.fumo.value)
                continue
                
        
        self.debug(self.driver.current_url, 'went to their webpage')
        self.idle(PRODUCT_DETAIL_ADD_CART_8)
        self.debug(self.driver.current_url, 'clicked add to cart')
        #WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, PRODUCT_DETAIL_ADD_CART_8))).click()
        #WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, CART_SUBMIT))).click()
        self.idle(CART_SUBMIT)
        self.debug(self.driver.current_url, 'clicked cart submit')
        #self.login()
    
    def confirm_purchase(self):
        self.idle(CART_MATOME_1_SUBMIT)
        self.debug(self.driver.current_url, 'confirmed item combo')
        #WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, CART_MATOME_1_SUBMIT))).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, CREDIT_CARD_LABEL))).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, SHIPPING_METHOD_LABEL))).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, CART_MATOME_2_SUBMIT))).click()
        self.debug(self.driver.current_url, 'confirmed purchase')
        #WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, CART_MATOME_3_SUBMIT))).click()
    
    def idle(self, btn):
        while True:
            try:
                wait = 5
                WebDriverWait(self.driver, wait).until(EC.element_to_be_clickable((By.CSS_SELECTOR, btn))).click()
                #WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, btn))).click()
                break
            except TimeoutException:
                self.driver.refresh()
                wait = 10
                print(self.fumo.name, end='')
                print(' refreshed at '+ btn + 'at ' + self.driver.current_url)
                continue
            except Exception as e:
                self.debug(self.driver.current_url, ' bugged out in idle')
                print(e)
                continue

    def check_for_error(self):
        sleep(1.25)
        #print(self.driver.current_url)
        if self.driver.current_url != PROCEED_TO_CHECKOUT_PAGE:
            print(self.fumo.name, end='')
            print(' errored')
            self.run()
        else:
            pass

    def debug(self, webpage, icon):
        print(self.fumo.name, end='')
        print(' got to ' + webpage + ' and ' + icon)