from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import urllib.request

# Define the Chrome profile path
CHROME_PROFILE_PATH = r'user-data-dir=C:\\Users\\<username>\\AppData\\Local\\Google\\Chrome\\User Data\\Whatsapp'

# Set up Chrome options with the profile path
options = webdriver.ChromeOptions()
options.add_argument(CHROME_PROFILE_PATH)


# Function to check if a WhatsApp contact exists and save their profile image
def whatsapp_checker(number):
    # Initialize the Chrome driver with the specified options
    browser = webdriver.Chrome(options=options)
    browser.maximize_window()

    # Open WhatsApp Web with the given phone number
    browser.get(f'https://web.whatsapp.com/send?phone={number}')

    try:
        # Wait for the profile image to appear on the page
        find_profile = WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/header')))

        # Click on the profile image to open the contact's profile
        find_profile.click()
        time.sleep(0.5)

        try:
            # Wait for the larger profile image to appear
            big_image = WebDriverWait(browser, 1).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="app"]/div/div/div[6]/span/div/span/div/div/section/div[1]/div[1]/div/img')))

            # Retrieve the profile image's source and save it to a file
            urllib.request.urlretrieve(big_image.get_attribute("src"), f'Whatsapp_{number}.jpg')
        except:
            # Return True to indicate that the contact exists
            print(f'{number} uses whatsapp, but does not have an avatar')
            return True

        print(f'{number} uses whatsapp. Avatar downloaded')
        return True
    except Exception as e:
        # Return False if the contact doesn't exist or there's an error
        print(e)
        return False
    finally:
        # Close the browser when you're done
        browser.quit()


# print(whatsapp_checker('Your_phonenumber'))
