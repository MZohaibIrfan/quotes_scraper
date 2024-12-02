import json
import time
import ssl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller


# setting up ssl here for verification purposes
ssl._create_default_https_context = ssl._create_unverified_context

#install correct chrome_driver
chromedriver_autoinstaller.install()


def start_browser():
    'launch the browser'
    options = webdriver.ChromeOptions()
    #use for webscraping, dispaly not needed 
    options.add_argument("--headless")
    # also not that necessary for webscarping
    options.add_argument("--diasable-gpu")

    #initialize a new chrome browser intsance with the options as described above
    driver = webdriver.Chrome(options=options)
    #return the driver
    return driver


def login_the_page(driver):
    #url to scrape
    url = "http://quotes.toscrape.com/login"
    #go to login page of the url
    driver.get(url)

    # Wait for the username field to appear and input dummy username
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    ).send_keys("dummy_user")
    #wait for password field and then input the dummy password
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password"))
    ).send_keys("dummy_password")
    
    # Wait for and click the login button using the input element's value
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@value='Login']"))
    ).click()

    # add delay so we wait for the next page to appear and then extract quotes
    time.sleep(5)


def extract_quotes(driver):
    # initialize empty list to store the quotes data
    quotes_data = []
    # find all elemnts that have the class name of quote but limit to first 20
    quotes_elements = driver.find_elements(By.CLASS_NAME, "quote")[:20]

    # loop over each quote element
    for quote_element in quotes_elements:
        # get the quote_text
        quote_text = quote_element.find_element(By.CLASS_NAME, "text").text

        # get the author name
        author = quote_element.find_element(By.CLASS_NAME, "author").text

        # get the author's page
        author_link = quote_element.find_element(By.TAG_NAME, "a").get_attribute("href")

        tags = []
        for tag_element in quote_element.find_elements(By.CLASS_NAME,"tag"):
            tags.append(tag_element.text)

        # Append to list in the format required
        quotes_data.append({
            "quote": quote_text,
            "author": author,
            "author_link": author_link,
            "tags": tags,
        })
    # return the quotes_data list
    return quotes_data


# Step 4: Save data to JSON
def save_to_json(data, filename="quotes.json"):

    #open file for write
    with open(filename, "w", encoding="utf-8") as f:
        #write in json format
        json.dump(data, f, indent=4, ensure_ascii=False)

# Main Execution
if __name__ == "__main__":
    # Initialize the browser
    driver = start_browser()

    try:
        # Login to the page, calls the function with the driver that it got at initialize browser
        login_the_page(driver)

        # Scrape the quotes and save in quotes
        quotes = extract_quotes(driver)

        # Save the quotes to a JSON file
        save_to_json(quotes)

        #letting you know task done
        print("Quotes scraped and saved successfully!")
    finally:
        # Close the browser
        driver.quit()