from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import yaml


def write_in_file(text, name="log.txt"):
    if name == "log.txt":
        local_time = time.localtime()  # get struct_time
        str_time = time.strftime("%d/%m/%Y, %H:%M:%S", local_time)
        text = str_time + "\n" + text
    with open(name, "w") as f:
        f.writelines(text)


try:
    try:
        conf = yaml.safe_load(open('conf.yml'))
        myEmail = conf['user']['email']
        myPassword = conf['user']['password']
        url_login = conf['url']['login']
        url_find = conf['url']['find']
    except:
        raise Exception("Smth wrong with conf")
    # options for browser keeps open after finish script
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
except Exception as error:
    write_in_file(str(error))
    exit()


def login(url, usernameId, username, passwordId, password, submit_button):
    driver.get(url)
    driver.find_element(By.ID, usernameId).send_keys(username)
    driver.find_element(By.ID, passwordId).send_keys(password)
    driver.find_element(By.NAME, submit_button).click()
    # if login is failed, server returns the same page with login form
    if driver.current_url == "https://xxx":
        raise Exception("Error: Login failed. Invalid credentials.")


# Create list of str "name + & + link".
# & is as a custom separator for Google Sheet to split text to columns "name" and "link".
# In Google sheet use function HYPERLINK (convert text to a hyperlink)


def find_elements(url) -> list:
    i = 1
    names_and_links = []
    # continue findind while exist needed element in DOM.
    while True:
        driver.get(f"{url}?page={i}")
        element = driver.find_element(
            By.ID, "table-container").find_element(By.TAG_NAME, "tbody")
        elements = element.find_elements(By.TAG_NAME, value="tr")
        if elements:
            for e in elements:
                names_and_links.append(e.find_element(By.TAG_NAME, value="td").text +
                                       "&" +
                                       e.get_attribute("data-link").replace("/admin", "") +
                                       "\n")
            i += 1
        else:
            break
    return names_and_links
