from selenium import webdriver
from login import do_login
from modifyitems import do_modify_items
from ultis import get_users_info
import time
import logging
from selenium.webdriver.chrome.service import Service

from dotenv import load_dotenv
import os

from typing import Union

# Load environment variables from .env file
load_dotenv()

PATH_CHROME = os.getenv("PATH_CHROME")
PATH_PROFILE = os.getenv("PATH_PROFILE")

print(PATH_CHROME)
print(PATH_PROFILE)


logging.basicConfig(
    filename='logs/app.log', 
    filemode='w', 
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
)

# PATH_CHROME = "C:\src\source\chromedriver-win64\chromedriver.exe"
# PATH_CHROME = "/Users/huanhoang/Downloads/source/chromedriver"

# #PATH_PROFILE = "C:/Users/My/AppData/Local/Google/Chrome/User Data/"
# PATH_PROFILE = "Users/huanhoang/Library/Application Support/Google/Chrome/"

LISTING_PAGE = "https://www.airbnb.com/hosting/listings"


def main() -> None:

    users: list[dict[str, Union[int, str]]] = get_users_info()

    for user in users:

        name: str = user['name']
        email: str = user['email']
        pwd: str = user['pwd']
        profile: str = user['profile']

        options = webdriver.ChromeOptions()

        service = Service(executable_path=PATH_CHROME)
        
        options.add_argument(f"--user-data-dir={PATH_PROFILE}{profile}")

        driver = webdriver.Chrome(
            service=service,
            # executable_path="C:\src\source\chromedriver-win64\chromedriver.exe",
            options=options 
        )
        # driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        driver.get(LISTING_PAGE)

        do_login(driver, email, pwd)

        # if name == 'account1':
        #     continue

        try_num: int = 1

        while try_num <= 6:
            try:
                do_modify_items(driver, name)
                logging.info(f'{name} is done.')
                print(f'{name} is done.')
                try_num = 1
                break
            except Exception as e:
                try_num += 1
                print(e)
                logging.error(e)
                print('Something went wrong. Retrying again {} times'.format(try_num))
                logging.info('Trying again.')
                time.sleep(15)
                driver.get(LISTING_PAGE)
                continue
        driver.quit()


if __name__ == "__main__":
    main()
