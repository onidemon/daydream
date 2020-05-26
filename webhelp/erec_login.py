from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep


class ErecBot():
    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def login(self):
        self.driver.get('https://erec.webhelp.fr/Login.aspx')
        
        sleep(2)
        
        username = self.driver.find_element_by_xpath('//*[@id="txt_userName"]')
        username.send_keys('dasultu-chiochiu')
        password = self.driver.find_element_by_xpath('//*[@id="txt_password"]')
        password.send_keys('Cbouabdo@2')
        sleep(2)
        login_btn = self.driver.find_element_by_xpath('//*[@id="bt_login"]').click()
    
    
    def start(self):
        
        project = self.driver.find_element_by_xpath('//*[@id="main_content_ddl_project"]/option[3]').click()
        activity = self.driver.find_element_by_xpath('//*[@id="main_content_ddl_activity"]/option[10]').click()
        start_btn =self.driver.find_element_by_xpath('//*[@id="main_content_bt_startChange"]').click()



bot = ErecBot()
bot.login()
bot.start()