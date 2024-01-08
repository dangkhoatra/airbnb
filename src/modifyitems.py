from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from ultis import parse_text_get_numbers, modify_text, parse_href_to_get_listingid

from sys import platform

import time

from logging_config import configure_logger

from log import write_file, read_file


logger = configure_logger()


def do_modify_items(driver: WebDriver, account: str):

    wait = WebDriverWait(driver, 30)

    click_to_detail_listing(wait)
    
    load_items_listing(driver, wait, account)


def click_to_detail_listing(wait):
    print('Starting list items')
    list_element = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="listings-table"]/tbody[2]/tr[1]/td[2]/a')
    ))
    list_element.click()
    logger.info('Click to load items succesful.')
    time.sleep(2)


def load_items_listing(driver: WebDriver, wait: WebDriverWait, account: str):

    no, items_edited= read_file(account)

    while True:
        
        nav_paing = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="panel-layout"]/div/div/div/section[1]/div/div/div[2]/div[3]/nav'),
            )
        )

        logger.info('Get nav paging success ful.', nav_paing)

        element_paging = nav_paing.find_element(By.XPATH, './div[1]/div[1]')

        first, last, total = parse_text_get_numbers(element_paging.text)

        for i in range(1, last - first + 1):
            item = wait.until(EC.element_to_be_clickable((
                By.XPATH, f'//*[@id="listings-table"]/tbody[2]/tr[{i}]/td[2]/a'))
                            )
            # print(item.get_attribute('outerHTML'))
            # input()

            href = item.get_attribute('href')
            id_item = parse_href_to_get_listingid(href)
            item_title = item.get_attribute('aria-label').split('.')[0]
            print(item_title)
            
            if id_item not in items_edited:
                no += 1
                item.click()
                print(f'# Starting edit - {item_title}')
                modify(driver, wait, href)
                item_desc = f"{no} ## {id_item} ## {item_title}"
                write_file(account, item_desc)
            else:
                print(f'# {item_title} is modified.')
            # input()
        
        if last == total:
            break
        else:
            btn_next_page = nav_paing.find_element(By.CSS_SELECTOR, 'button[aria-label="Next page"]')
            btn_next_page.click()
            time.sleep(5)
            print('Continue to next page')
            continue
    
    # for item in items_listing:
    #     print(item.get_attribute('outerHTML'))
    #     time.sleep(1)

    return

def get_number_items_per_page(wait: WebDriverWait):

    nav_paging = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="panel-layout"]/div/div/div/section[1]/div/div/div[2]/div[3]/nav'),
        )
    )

    return nav_paging # parse_text_get_numbers(element.text)


def modify(driver: WebDriver, wait: WebDriverWait, href: str) -> None:
    try_get_title: int = 1

    while try_get_title <= 3:
        try:
            title_detail = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="manage-your-space-header"]'),
                )
            )
            break
        except:
            print('Refresh page for get listing detail.')
            driver.refresh()
            try_get_title += 1
            continue
            # title_detail = wait.until(EC.presence_of_element_located(
            #     (By.XPATH, '//*[@id="manage-your-space-header"]'),
            # ))


    item_title = title_detail.text

    # print(f'Modyfing {item_title}')

    edit_photo(driver, wait, href)

    edit_title(wait)

    edit_descriptions(driver, wait)
    
    print(f'Done. {item_title}')

    time.sleep(1)

def edit_photo(driver: WebDriver, wait: WebDriverWait, href: str) -> None:

    # print('Starting edit photo.')

    photos = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '#photos')
    ))
    edit_photos = photos.find_element(By.CSS_SELECTOR, 'a[aria-label="Edit Photos"]')
    edit_photos.click()
    btns_edit = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'button[aria-label="Photo options"]')
        )
    )
    if len(btns_edit) >= 2:
        btn_2nd_edit = btns_edit[1]
        btn_2nd_edit.click()
        btn_set_cover_photo = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button[aria-label="Make cover photo"]')
            )
        )
        btn_set_cover_photo.click()
        time.sleep(1)
        # print(f'a[href="{href}"]')
        back = driver.find_elements(By.TAG_NAME, 'a')
        for a in back:
            if a.get_attribute("href") == href:
                a.click()
                print('- Done edit photo.')
                break
        time.sleep(1.5)
    else:
        return
    
def edit_title(wait: WebDriverWait) -> None:
    title_element = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#listing-basics')
        )
    )

    edit_title = title_element.find_element(
        By.CSS_SELECTOR,
        'button[aria-label="Edit Listing title"]'
    )

    edit_title.click()

    time.sleep(1)

    listing_title = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[aria-label="Listing title"]')
        )
    )

    input_elements = listing_title.find_elements(
        By.TAG_NAME, 'input'
    )

    is_save: bool = False

    for inp_ele in input_elements:
        title = inp_ele.get_attribute("value").strip()
        if len(title) > 0:
            clear(inp_ele)
            modified_text: str = modify_text(title)
            inp_ele.send_keys(modified_text)
            updated_text = inp_ele.get_attribute('value')
            if updated_text == modified_text:
                time.sleep(0.25)
                # Do additional verification or actions if needed
            else:
                raise ValueError('Something went wrong.')
                print("Text modification was not successful.")
            if is_save == False:
                is_save = True

    if is_save:

        btn_save = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button[aria-label="Save Listing title"]')
            )
        )

        btn_save.click()
        print('- Done edit title.')

    else:

        btn_cancle = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button[aria-label="Cancel Listing title"]')
            )
        )
        btn_cancle.click()
        print('- Cancle edit title.')

    time.sleep(2)


def edit_descriptions(driver: WebDriver, wait: WebDriverWait) -> None:

    listing_description = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#listing-description')
        )
    )

    is_save: bool = False

    #print(listing_description.get_attribute("outerHTML"))

    btn_edit = listing_description.find_element(
        By.CSS_SELECTOR,
        'button[aria-label="Edit Listing description"]'
    )

    btn_edit.click()
    time.sleep(0.75)

    text_areas = driver.find_elements(By.TAG_NAME, 'textarea')

    for text_area in text_areas:
        # print(text_area.get_attribute('outerHTML'))
        text: str = text_area.text.strip()
        if len(text) > 0:
            clear(text_area)
            modified_text: str = modify_text(text)
            # driver.execute_script(f'arguments[0].value = "{modify_text(text)}";', text_area)
            text_area.send_keys(modified_text)

            updated_text = text_area.get_attribute('value')  # Get the updated value attribute
            if updated_text == modified_text:
                time.sleep(0.25)
                # Do additional verification or actions if needed
            else:
                raise ValueError('Something went wrong.')
                print("Text modification was not successful.")
            #update_description(text_area, text)
            # time.sleep(0.75)
            # input()
            if is_save == False:
                is_save = True

    if is_save:
        btn_save = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button[aria-label="Save Listing description"]')
            )
        )
        btn_save.click()
        print('- Done edit description.')
    else:
        btn_cancle = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button[aria-label="Cancel Listing description"]')
            )
        )
        btn_cancle.click()
        print(print('- Cancle edit description.'))

    time.sleep(2)



def update_text(element, text: str):
    text = text.strip()
    if text[-1] == '.':
        element.click()
        element.send_keys(Keys.END)
        time.sleep(1)
        element.send_keys(Keys.BACKSPACE)
    else:
        element.send_keys('.')


def update_description(element, text: str):
    if text[-1] == '.':
        element.click()
            # time.sleep(1)
        time.sleep(0.1)
        for _ in range(12):

            element.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.1)
        # Delete the last character
        element.send_keys(Keys.BACKSPACE)
    else:
        element.send_keys('.')


def clear(elem):
  elem.send_keys((Keys.COMMAND if platform == "darwin" else Keys.CONTROL) + "a")
  elem.send_keys(Keys.DELETE)
    
    
    
    

    
    

    

    