import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture
def browser_url():
    return "https://genxflo.com/login"

@pytest.fixture
def valid_credentials():
    return {"username": "", "password": ""}

@pytest.fixture
def incorrect_password():
    return "wrongpassword"

@pytest.fixture
def incorrect_username():
    return "wronguser@gmail.com"

def test_valid_login(browser, browser_url, valid_credentials):
    browser.get(browser_url)

    username_input = browser.find_elements(By.CLASS_NAME, "Input-Field")[0]
    password_input = browser.find_elements(By.CLASS_NAME, "Input-Field")[1]
    login_button = browser.find_element(By.CLASS_NAME, "login-button")

    username_input.send_keys(valid_credentials["username"])
    password_input.send_keys(valid_credentials["password"])
    login_button.click()
   
    expected_title = "Genxflo - Nextflow Bioinformatics Pipeline Builder" 
    assert expected_title in browser.title, f"Expected '{expected_title}' in title, but got '{browser.title}'"

def test_invalid_password(browser, browser_url, valid_credentials, incorrect_password):
    """Correct username but incorrect password"""
    browser.get(browser_url)

    username_input = browser.find_elements(By.CLASS_NAME, "Input-Field")[0]
    password_input = browser.find_elements(By.CLASS_NAME, "Input-Field")[1]
    login_button = browser.find_element(By.CLASS_NAME, "login-button")

    username_input.send_keys(valid_credentials["username"])
    password_input.send_keys(incorrect_password)
    login_button.click()

    # error_message = browser.find_element(By.CLASS_NAME, "error-message-login")
    error_message = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "error-message-login"))
)
    assert error_message.is_displayed(), "Error message is not displayed!"
    assert "Wrong Email or Password" in error_message.text, f"Unexpected error message: {error_message.text}"

def test_invalid_username(browser, browser_url, incorrect_username, valid_credentials):
    """Incorrect username but correct password"""
    browser.get(browser_url)

    username_input = browser.find_elements(By.CLASS_NAME, "Input-Field")[0]
    password_input = browser.find_elements(By.CLASS_NAME, "Input-Field")[1]
    login_button = browser.find_element(By.CLASS_NAME, "login-button")

    username_input.send_keys(incorrect_username)
    password_input.send_keys(valid_credentials["password"])
    login_button.click()

    error_message = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "error-message-login"))
)
    assert error_message.is_displayed(), "Error message is not displayed!"
    assert "User not found" in error_message.text, f"Unexpected error message: {error_message.text}"