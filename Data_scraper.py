from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

service = Service(executable_path="/path/to/chromedriver")
driver = webdriver.Chrome(service=service)
driver.get("https://www.lego.com/en-gb")
assert "Python" in driver.title

elem = driver.find_element(By.NAME, "q")

elem.clear()
elem.send_keys("pycon")
elem.semd_keys(Keys.RETURN)

assert "No results found." not in driver.page_source
driver.close()
