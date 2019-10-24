from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
import re
from selenium.webdriver.common.keys import Keys


def get_inputs():
    class_name = input("What is the class?: ")
    class_number = input("What is the class number?: ")
    search(class_name, class_number)


def search(name, number):
    class_url = "https://webapp4.asu.edu/catalog/classlist"
    prof_url = "https://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Arizona+State+University&schoolID=45&queryoption=TEACHER"
    class_browser = webdriver.Chrome("./chromedriver.exe")
    prof_browser = webdriver.Chrome("./chromedriver.exe")

    class_browser.get(class_url)
    prof_browser.get(prof_url)

    subject_input = class_browser.find_element_by_id("subjectEntry")
    number_input = class_browser.find_element_by_id("catNbr")
    submit_button = class_browser.find_element_by_id("go_and_search")

    search_bar = prof_browser.find_element_by_id("professor-name")

    time.sleep(1)

    subject_input.send_keys(name)
    number_input.send_keys(number)
    submit_button.click()

    time.sleep(1)

    class_response = requests.get(class_browser.current_url)

    class_soup = BeautifulSoup(class_browser.page_source, "html.parser")

    raw_names = class_soup.find_all("a", class_="nametip")

    prof_names = []
    for i in raw_names:
        link = i.get("href")
        arr = re.split(r"&sp=S", link)
        name = arr[5] + " " + arr[6]
        prof_names.append(name)

    prof_names = list(dict.fromkeys(prof_names))

    for i in prof_names:
        search_bar.send_keys(i)
        time.sleep(1)
        results = prof_browser.find_element_by_class_name("result-list")
        try:
            i += " " + prof_browser.find_element_by_class_name("rating").text
        except:
            i += " Not on Rate My Professors"
        search_bar.clear()
        print(i)
    input("ENTER to close...")


if __name__ == "__main__":
    get_inputs()