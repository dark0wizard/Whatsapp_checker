from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import urllib.request
import datetime
import csv

# Define the Chrome profile path
CHROME_PROFILE_PATH = r'user-data-dir=C:\\Users\\<username>\\AppData\\Local\\Google\\Chrome\\User Data\\Whatsapp'

# Set up Chrome options with the profile path
options = webdriver.ChromeOptions()
options.add_argument(CHROME_PROFILE_PATH)


def whatsapp_login():
    '''Uses this function only one time to login at the whatsapp account'''
    browser = webdriver.Chrome(options=options)
    browser.maximize_window()
    browser.get('https://web.whatsapp.com/')
    time.sleep(20)
    browser.quit()


def whatsapp_checker(numbers: list[str]) -> list[list]:
    '''Function to check if a WhatsApp contact exists and return WhatsApp`s account info:
    Phone number, using WhatsApp,about and profile image '''

    final_data = []

    # Initialize the Chrome driver with the specified options
    browser = webdriver.Chrome(options=options)
    browser.maximize_window()
    browser.get('https://web.whatsapp.com/')

    for number in numbers:
        if not number.startswith('+'):
            number = '+' + number
        # Open WhatsApp Web with the given phone number
        check_number = [number]
        browser.get(f'https://web.whatsapp.com/send?phone={number}')

        try:
            # Wait for the profile image to appear on the page
            find_profile = WebDriverWait(browser, 15).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/header')))

            check_number.append(True)
            # Click on the profile image to open the contact's profile
            find_profile.click()
            time.sleep(1)

            try:
                # Copy what the profile info
                about = WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[2]/div[5]/span/div/span/div/div/section/div[2]/span/span')))
                check_number.append(about.text)
            except:
                check_number.append(False)

            try:
                # Wait for the larger profile image to appear
                big_image = WebDriverWait(browser, 1).until(EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[1]/div/div/div[2]/div[5]/span/div/span/div/div/section/div[1]/div[1]/div/img')))

                # Retrieve the profile image's source
                check_number.append(big_image.get_attribute("src"))

                # To download profile picture
                urllib.request.urlretrieve(big_image.get_attribute("src"), f'Whatsapp_{number}.jpg')
            except:
                check_number.append(False)
        except:
            # Add a list of False if the contact doesn't exist
            check_number += [False, False, False]

        final_data.append(check_number)
    browser.quit()
    return final_data


def write_data_in_csv(data):
    '''This function saves info about WhatsApp account in a csv file'''
    today_date = datetime.datetime.now()
    filename = today_date.strftime("%Y-%m-%d_%H-%M") + ".csv"
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(["Phone number", "Whatsapp", "About", "Picture"])
        writer.writerows(data)


def main():
    whatsapp_login()  # Use only one time
    result = whatsapp_checker(['your phone number1', 'your phone number2'])
    write_data_in_csv(result)


if __name__ == '__main__':
    main()
    
