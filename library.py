from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import sys

library_id = input("Please enter your library ID: ")
library_pin = input("Please enter your PIN: ")

print("Now running...")

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(executable_path = "./chromedriver", chrome_options = chrome_options)
driver.get("https://catalog.colapl.org/uhtbin/cgisirsi/0/0/0/1/1168/X")

print("Reached login page.")

login = driver.find_element_by_css_selector('form[name=loginform]')
login.find_element_by_id('user_id').send_keys(library_id)
login.find_element_by_id('password').send_keys(library_pin)
login.find_element_by_class_name('login_button').click()

# Check if there was an error.
delay = WebDriverWait(driver, 10)
delay.until(lambda driver: driver.current_url != "https://catalog.colapl.org/uhtbin/cgisirsi/0/0/0/1/1168/X")

if len(driver.find_elements_by_css_selector(".content_container.error")) > 0:
    print("There's an error with the login request. Please double-check your library # and PIN.")
    driver.close()
    sys.exit()

print("Login successful.")

driver.find_element_by_partial_link_text("Renew materials. Manage holds. Pay bills.").click()

books = []
print("Pulling books from the catalog...")

form = driver.find_element_by_id("renewcharge")
for book in form.find_elements_by_tag_name("tr"):
    book_fields = book.find_elements_by_css_selector("td.accountstyle")
    title_extended = book_fields[0].find_element_by_tag_name("label")
    books.append({
        "title": title_extended.text.split("/")[0].strip(),
        "author": title_extended.text.split("/")[1].strip(),
        "category": book_fields[1].text,
        "due": book_fields[3].text,
        "times_renewed": 0 if len(book_fields[2].text) == 0 else int(book_fields[2].text)
    })

print "Done."
driver.close()

for b in books:
    print b
