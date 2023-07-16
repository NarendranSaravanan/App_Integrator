import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def login_to_instagram(username, password):
    # Set up the Selenium webdriver
    options = Options()
    options.add_argument("--headless")  # Run Chrome in headless mode (without opening a browser window)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Open Instagram login page
    driver.get("https://www.instagram.com/accounts/login/")

    # Fill in the login form
    username_field = driver.find_element(By.NAME, "username")
    username_field.send_keys(username)
    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys(password)

    # Submit the login form
    login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
    login_button.click()

    # Wait for the page to load
    driver.implicitly_wait(5)

    # Display the Instagram page
    st.image(driver.get_screenshot_as_png(), caption='Instagram Page')

    # Close the webdriver
    driver.quit()

def main():
    choice = st.sidebar.radio("Select an option", ("Instagram", "Facebook", "LinkedIn"))
    if choice == "Instagram":
        st.title("Instagram Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
    
        if st.button("Login"):
            login_to_instagram(username, password)
    elif choice == "Facebook":
        st.title("Facebook Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
    
        if st.button("Login"):
            login_to_instagram(username, password)
    elif choice == "LinkedIn":
        st.title("LinkedIn Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
    
        if st.button("Login"):
            login_to_instagram(username, password)

if __name__ == "__main__":
    main()
