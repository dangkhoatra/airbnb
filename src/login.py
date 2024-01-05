from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver

import time

LOGGED_TITLE_EN: str = 'Manage your listing'
LOGGED_TITLE_VI: str = 'Quản lý mục cho '
LOGIN_TITLE_EN: str = 'Log In'
LOGIN_TITLE_VI: str = 'Đăng '


def do_login(driver: WebDriver, email: str, pwd: str) -> None:

    if LOGIN_TITLE_EN in driver.title or LOGIN_TITLE_VI in driver.title:
        input_login(driver, email, pwd)
        print('Login successful.')
        return
    elif LOGGED_TITLE_EN in driver.title or LOGGED_TITLE_VI in driver.title:
        print('Logged.')
        return
    else:
        input()
        raise ValueError('Something Error.')


def input_login(driver: WebDriver, email: str, pwd: str) -> None:

    wait = WebDriverWait(driver, 15)  # Initialize WebDriverWait with a timeout of 10 seconds
    
    # Example usage of the provided XPath
    welcome_element = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="panel-header"]/section/h2/div')
    ))

    if 'Welcome back' in welcome_element.text or 'Chào mừng' in welcome_element.text:
        print('Login again')
        login_again(wait, email, pwd)
    else:
        print('First login')
        first_login(wait, email, pwd)
    
    if 'Manage your listing' in driver.title:
        return
    else:
        waiting_submit_code(driver)
        return
    

def first_login(wait: WebDriverWait, email: str, pwd: str) -> None:
    
    btn_login_email = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'button[data-testid="social-auth-button-email"]')
    ))
    btn_login_email.click()

    time.sleep(2)

    input_email = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'input[name="user[email]"]')
    ))
    input_email.send_keys(email)

    time.sleep(2)

    btn_submit_login = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'button[data-testid="signup-login-submit-btn"]')
    ))
    btn_submit_login.click()

    time.sleep(2)

    input_pwd = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'input[name="user[password]"]')
    ))
    input_pwd.send_keys(pwd)
    time.sleep(2)

    btn_login = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'button[data-testid="signup-login-submit-btn"]')
    ))
    btn_login.click()
    time.sleep(2)
    print('Login in first time successful.')


def login_again(wait: WebDriverWait, email: str, pwd: str) -> None:

    input_email = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="email"]')
    ))
    input_email.clear()
    input_email.send_keys(email)
    time.sleep(1)

    input_pwd = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="password"]')
    ))
    input_pwd.send_keys(pwd)
    time.sleep(1)

    btn_login = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="FMP-target"]/div/div/div[3]/form/div[3]/button')
    ))
    btn_login.click()
    time.sleep(1)


def waiting_submit_code(driver: WebDriver) -> None:
    while True:
        if LOGGED_TITLE_EN in driver.title or LOGGED_TITLE_VI in driver.title:
            break
        else:
            print('Waiting user submit code')
            time.sleep(10)
            continue
