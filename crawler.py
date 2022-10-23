from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from webdriver_manager.chrome import ChromeDriverManager

base_url = 'http://place.map.kakao.com/'

def extract_menu(id_list):
    full_menu = dict()  # 모든 가게의 메뉴
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service)
    for id in id_list:
        menu_list = dict()
        browser.get(base_url + id)
        time.sleep(1)
        soup = BeautifulSoup(browser.execute_script('return document.body.innerHTML'), 'html.parser')
        menu = soup.find("ul", class_="list_menu")
        if not menu:
            full_menu[id] = menu_list
            continue
        coffees = menu.find_all('li', recursive=False)
        for coffee in coffees:
            if coffee.find("em", class_="price_menu") is None:
                break
            price = int(coffee.find("em", class_="price_menu").contents[-1].replace(',', ''))
            name = coffee.find("span", class_="loss_word").string
            menu_list[name] = price
        full_menu[id] = menu_list
    browser.quit()
    return full_menu
