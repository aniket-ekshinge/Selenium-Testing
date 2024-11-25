from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Setup WebDriver
def setup_module(module):
    global driver
    # Set up the Chrome WebDriver using Service
    service = Service(ChromeDriverManager().install())  # Automatically installs the ChromeDriver
    driver = webdriver.Chrome(service=service)  # Initialize WebDriver with the Service object
    driver.get("http://localhost:5000/")

def teardown_module(module):
    driver.quit()

# Integration Test: Add and Issue Book
def test_add_and_issue_book():
    # Add a book
    driver.get("http://localhost:5000/add-book")
    driver.find_element(By.ID, "title").send_keys("Integration Book")
    driver.find_element(By.ID, "author").send_keys("Author Name")
    driver.find_element(By.ID, "isbn").send_keys("444444")
    driver.find_element(By.TAG_NAME, "button").click()

    # Issue the book
    driver.get("http://localhost:5000/issue-book")
    driver.find_element(By.ID, "book_id").send_keys("1")
    driver.find_element(By.ID, "issued_to").send_keys("Jane Doe")
    driver.find_element(By.TAG_NAME, "button").click()

    # Verify the issued status from the database (Manually or use DB connection)

# Integration Test: Issue and Return Book
def test_issue_and_return_book():
    # Issue a book
    driver.get("http://localhost:5000/issue-book")
    driver.find_element(By.ID, "book_id").send_keys("1")
    driver.find_element(By.ID, "issued_to").send_keys("Jane Doe")
    driver.find_element(By.TAG_NAME, "button").click()

    # Return the book
    driver.get("http://localhost:5000/return-book")
    driver.find_element(By.ID, "book_id").send_keys("1")
    driver.find_element(By.TAG_NAME, "button").click()

    # Verify the return status from the database (Manually or use DB connection)
