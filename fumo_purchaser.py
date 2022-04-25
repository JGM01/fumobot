from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# CSS Selectors 
WEBSITE = 'https://secure.amiami.com/eng/'
PRODUCT_DETAIL_ADD_CART_8 = '[data-kanshi="productDetailAddCart8"]'
CART_SUBMIT = '[data-kanshi="cartSubmit"]'
CART_MATOME_1_SUBMIT = '[data-kanshi="cartMatome1Submit"]'
CART_MATOME_2_SUBMIT = '[data-kanshi="cartMatome2Submit"]'
CART_MATOME_3_SUBMIT = '[data-kanshi="cartMatome3Submit"]'


class FumoPurchaser:
    def __init__(self, fumo, username, password):
        self.driver = webdriver.Firefox()
        self.fumo = fumo
        self.username = username
        self.password = password

    def execute(self):
        self.driver.get(WEBSITE)
        self.login()
        self.purchase_fumo()
        self.confirm_purchase()
    
    def login(self):
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.NAME, 'email'))).send_keys(self.username)
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.NAME, 'password'))).send_keys(self.password)
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-submit'))).click()
        
    def purchase_fumo(self):
        self.driver.get(self.fumo)
        self.idle()
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, PRODUCT_DETAIL_ADD_CART_8))).click()
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, CART_SUBMIT))).click()
        self.login()
    
    def confirm_purchase(self):
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, CART_MATOME_1_SUBMIT))).click()
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//label[contains(text(), "Credit card")]'))).click()
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[class='form-radio-label'][for='shipping-method19'] span"))).click()
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, CART_MATOME_2_SUBMIT))).click()
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, CART_MATOME_3_SUBMIT))).click()
    
    def idle(self):
        while True:
            try:
                WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, PRODUCT_DETAIL_ADD_CART_8)))
                break
            except TimeoutException:
                self.driver.refresh()
                continue