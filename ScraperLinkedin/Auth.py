from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from time import sleep


def login(driver: Chrome, user: str, pwd: str) -> None:
    
    '''
    Open Bronswer, and put the link and credentials
    '''

    driver.get('https://www.linkedin.com/login')

    # Preencher credenciais
    email = driver.find_element(By.ID, 'username')
    email.send_keys(user)
    password = driver.find_element(By.ID, 'password')
    password.send_keys(pwd)
    password.submit()