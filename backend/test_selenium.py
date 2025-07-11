from selenium import webdriver

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
driver.get("https://recreation.gov")
input("Press Enter to quit...")
driver.quit()