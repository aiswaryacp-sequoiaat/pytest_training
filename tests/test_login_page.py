import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture
def browser_url():
    return "https://practicetestautomation.com/practice-test-login/"

@pytest.fixture
def valid_credentials():
    return {"username": "student", "password": "Password123"}

def test_valid_login(browser, browser_url, valid_credentials):
    browser.get(browser_url)

    username_input = browser.find_element(By.ID, "username")
    password_input = browser.find_element(By.ID, "password")
    login_button = browser.find_element(By.ID, "submit")

    username_input.send_keys(valid_credentials['username'])
    password_input.send_keys(valid_credentials['password'])

    login_button.click()

    expected_title = "Logged In Successfully"
    assert expected_title in browser.title, f"Expected '{expected_title}' in title, but got '{browser.title}'"