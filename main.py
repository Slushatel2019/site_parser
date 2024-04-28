from selenium.common.exceptions import NoSuchElementException
from base import *


try:
    autologin = login(url_login, "user_email", myEmail,
                      "user_password", myPassword, "commit")
    try:
        finded_elements = find_elements(url_find)
    except NoSuchElementException as e:
        raise Exception(e.msg)
    write_in_file(finded_elements, "named_links.txt")
except Exception as error:
    driver.close()
    write_in_file(str(error))
