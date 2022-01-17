# -*- coding: utf-8 -*-
import pickle
import loguru
import requests
from bs4 import BeautifulSoup
from logging import info, log
import sys
from loguru import logger
import re
import base64
import regex
import time
import json
import psutil
from loguru import logger
from licensing.models import *
from licensing.methods import Key, Helpers
import psutil


# import os
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# import python libraries
import random
import string
from Crypto.Cipher import AES
from configparser import ConfigParser
import json
from requests.api import get
from requests.models import Response
from requests.sessions import session
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import ctypes
from pprint import pprint
from random import choice

with open("settings.json", "r", encoding="utf-8") as file:
    data = json.load(file)

key = data["settings"]["key"]

xf_user = data["cookie"]["xf_user"]
xf_tfa_trust = data["cookie"]["xf_tfa_trust"]

bot_token = data["telegram"]["BOT_TOKEN"]
chat_id = data["telegram"]["chat_id"]

prox = int(data["proxies"]["choice"])
prx = data["proxies"]["proxy"]

linx = data["settings"]["url"]
markup = data["settings"]["markup"]

bot_off = data["settings"]["bot_off"]

time_sleeping = int(data["settings"]["time_sleep"])

logger.debug(linx)


ses = requests.session()
ses.headers.update(
    {
        "upgrade-insecure-requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/85.0.4155.121 Safari/537.36 OPR/71.0.3770.284 (Edition Yx)",
    }
)


if int(prox) == 1:

    ses.proxies = {"http": f"http://{prx}", "https": f"http://{prx}"}

    r = ses.get("https://whoer.net/ru")
    soup = BeautifulSoup(r.text, "lxml")

    print(
        soup.find("div", {"class": "main-ip-info__ip"})
        .text.strip()
        .replace("\n\n\n\n", "\n")
    )


def checkforjsandfix(soup):

    noscript = soup.find("noscript")
    if not noscript:
        return False
    pstring = noscript.find("p")
    if not (
        pstring
        and pstring.string
        == "Oops! Please enable JavaScript and Cookies in your browser."
    ):
        return False
    script = soup.find_all("script")
    if not script:
        return False
    if not (
        script[1].string.startswith(
            'var _0xe1a2=["\\x70\\x75\\x73\\x68","\\x72\\x65\\x70\\x6C\\x61\\x63\\x65","\\x6C\\x65\\x6E\\x67\\x74\\x68","\\x63\\x6F\\x6E\\x73\\x74\\x72\\x75\\x63\\x74\\x6F\\x72","","\\x30","\\x74\\x6F\\x4C\\x6F\\x77\\x65\\x72\\x43\\x61\\x73\\x65"];function '
        )
        and script[0].get("src") == "/aes.js"
    ):
        return False

    value_encrypted = re.search(
        r"slowAES.decrypt\(toNumbers\(\"([0-9a-f]{32})\"\)", script[1].string
    ).group(1)
    cipher = AES.new(
        bytearray.fromhex("e9df592a0909bfa5fcff1ce7958e598b"),
        AES.MODE_CBC,
        bytearray.fromhex("5d10aa76f4aed1bdf3dbb302e8863d52"),
    )
    value = cipher.decrypt(bytearray.fromhex(value_encrypted)).hex()
    logger.debug("Импорт Cookie")
    ses.cookies.set_cookie(
        requests.cookies.create_cookie(
            domain="." + "lolz.guru", name="df_uid", value=value
        )
    )

    ses.cookies.set_cookie(
        requests.cookies.create_cookie(
            domain="." + "lolz.guru",
            name="xf_user",
            value=xf_user,
        )
    )

    ses.cookies.set_cookie(
        requests.cookies.create_cookie(
            domain="." + "lolz.guru",
            name="xf_tfa_trust",
            value=xf_tfa_trust,
        )
    )

    return True  # should retry


def get_xfToken():
    try:
        time.sleep(0.5)
        xf = ses.get("https://lolz.guru/")
        soup = BeautifulSoup(xf.text, "lxml")
        return soup.find("input", attrs={"name": "_xfToken"}).get("value")

    except Exception:
        time.sleep(3)


page = ses.get("https://lolz.guru/")
soup = BeautifulSoup(page.text, "html.parser")
checkforjsandfix(soup)

response = ses.get("https://lolz.guru/")
soup = BeautifulSoup(response.text, "html.parser")


def retrun_badges(link):
    r = ses.get(link)
    soup = BeautifulSoup(r.text, "lxml")
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(str(soup))
    try:

        price = soup.find("span", {"class": "value"}).text
    except:
        logger.error("Куки были введены неправильно или вообще не введены")
        return 0
    title = soup.find(
        "h1", {"class": "h1Style marketItemView--titleStyle"}).find("span").text
    thread_id = link.split("/")[4]
    logger.warning(f"{link} | {price} | {title} | {thread_id}")

    return_inf = [link, price, title, thread_id]
    return return_inf


def return_balance(count):

    response = ses.get("https://lolz.guru/")
    soup = BeautifulSoup(response.text, "html.parser")

    balik = soup.find("span", {"class": "balanceValue"}).text

    ctypes.windll.kernel32.SetConsoleTitleW(
        f" 𝘔𝘢𝘳𝘬𝘦𝘵𝘉𝘰𝘵 | 𝘉𝘢𝘭𝘢𝘯𝘤𝘦: {balik} | 𝘗𝘶𝘳𝘤𝘩𝘢𝘴𝘦: {count} "
    )
    logger.debug(f"BALANCE: {balik} руб.")

    return balik


def parse():
    global i_count
    i_count = 0
    checked_bot_off = 0
    while True:
        for link in linx:
            for b in markup:
                marks = b
            r = ses.get("https://lolz.guru")
            soup = BeautifulSoup(r.text, "lxml")
            balancee = return_balance(i_count)

            if int(balancee) <= 0:
                logger.error(
                    "У тебя баланс меньше 0, вернитесь когда баланс будет больше нуля"
                )
                time.sleep(15)
                sys.exit()
            try:
                response = ses.get(f"{link}").text
                logger.warning("Обновляю страницу")
                soup = BeautifulSoup(response, "lxml")
                # logger.success(soup)
                all_articles = soup.find_all(
                    "div", {"class": "marketIndexItem"})
                thread = {}
                uri_account = []
                for article in all_articles:
                    uri_account.append("https://lolz.guru/" + article.find(
                        "a", {"class": "marketIndexItem--Title"}).get("href"))
                global data
                try:
                    acx = choice(uri_account)
                    logger.warning(uri_account)
                    data = retrun_badges(acx)
                    logger.success(f"Покупаю аккант: {acx}")
                except Exception as ex:
                    logger.info(
                        f"Обновляю страницу")
                    time.sleep(time_sleeping)
                    continue
                result = int(marks) + int(data[1])
                if int(bot_off) >= int(checked_bot_off):
                    try:
                        buy(data[3], data[1], data[2], data[0], result)
                        checked_bot_off += 1
                    except Exception as ex:
                        logger.critical(
                            f"Ошибка на 242 строке, передайте кодеру\n{ex}")
                        time.sleep(5)
                        continue
                else:
                    logger.critical("Лимит покупок достигнут.")
                    time.sleep(1000)
                    sys.exit()
            except Exception as ex:
                logger.critical(
                    f"{ex}")
                time.sleep(20)
                continue
        time.sleep(time_sleeping)


def authorization():
    """protection"""
    RSAPubKey = "<RSAKeyValue><Modulus>pU0PoQ/j1pzWnji0EKpdrPfK8nuWVeEX7dI8UTkRewqGzMubOoKsSGWdopbFffqwSo8d3FVT6LC6wgXV/KLzL5PWB/pmYWhIxwyp6CWktJVkevSrAVZodcrQEzRVJFyP76OgtnWzplb8+Ecfx2oAAIbStrbbt+N6yTNxJlHZTiCMBMoIbnCT3mXdFOx2nSnkRHbkK/bbZgFRYYVQWYU1nM6lI8nIsOCv7xbrj8CkW5C/fmYTbdOHiYXkN2TdCUXlqMT70hygC9ihS5l/+VH46xMAV5Fth1oay0KmLOqLzVFqe/g4HfSo74E0xEktOpgc+T5hP/54Ney3rsy9yusGoQ==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"  # RSA токен
    access = "WyI5OTE0Nzc4IiwiZlJ5RG5wNDk0NG9hRDYyRTVRYStMMjhubFI4cGkyN0NPdk92ZjJiUSJd"  # Auth токен
    key1 = key
    for proc in psutil.process_iter():
        name = proc.name()
        if name == "HTTPDebuggerUI.exe":
            time.sleep(2)
            # exit(0)

    result = Key.activate(
        token=access,
        rsa_pub_key=RSAPubKey,
        product_id="13628",
        key=key1,
        machine_code=Helpers.GetMachineCode(),
    )

    if result[0] == None or not Helpers.IsOnRightMachine(result[0]):
        # ошибка и ее причина
        logger.info(f"Ключ не работает: {result[1]}")
        logger.info("Купить ключ у @Benefix")
        sys.exit()
    else:
        # Если ключ правильный:
        logger.info("Ключ верный!")
        # тут можно написать то, что будет происходить если ключ верный


def booking(thread_id, price, title, link):

    payload = {
        "price": price,
        "_xfRequestUri": f"/market/{thread_id}/",
        "_xfNoRedirect": "1",
        "_xfToken": get_xfToken(),
        "_xfResponseType": "json",
    }

    r = ses.get(
        f"https://lolz.guru/market/{thread_id}/balance/check?price={price}&&_xfRequestUri=%2Fmarket%2F{thread_id}%2F&_xfNoRedirect=1&_xfToken={get_xfToken()}&_xfResponseType=json",
        data=payload,
    ).text

    if "30" in r:
        logger.success("Успешно забронировал")


def buy(thread_id, price, title, link, marks):

    booking(thread_id, price, title, link)

    payload = {"_xfToken": get_xfToken(), "_xfConfirm": "1"}

    response = ses.post(
        f"https://lolz.guru/market/{thread_id}/confirm-buy", data=payload
    )

    logger.success("Аккаунт успешно приобретен")

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(
        ChromeDriverManager().install(), options=chrome_options)
    driver.maximize_window()
    driver.get(f"https://lolz.guru/market/{thread_id}/")
    time.sleep(2)
    driver.delete_all_cookies()
    for cookie in pickle.load(open("session", "rb")):
        driver.add_cookie(cookie)

    driver.refresh()

    time.sleep(4)
    try:
        login = driver.find_element_by_xpath(
            "//span[@id='loginData--login']").text
        password = driver.find_element_by_xpath(
            "//span[@id='loginData--password']").text
        category_id = driver.find_element_by_xpath(
            "//a[@class='button resellButton']"
        ).get_attribute("href")

        category_id = category_id.split("category_id=")[1]

        logger.success(f"{login}:{password} | {category_id}")
        time.sleep(2)

        data = f"""
        
        🗡 Купил аккаунт

        info: {login}:{password}
        login: {login}
        password: {password}
        
        ⚔ Ссылка на аккаунт: {link}
        👑 Название темы: {title}
        💸 Цена акканута: {price}



        """
        r = ses.get(
            f"https://api.telegram.org/bot{bot_token}/sendmessage?chat_id={chat_id}&text={data}"
        )

        resell(price, title, login, password, category_id, marks)
    except:
        pass


def resell(price, title, login, password, category_id, marks):
    r = ses.get(f"https://lolz.guru/market/item/add?category_id={category_id}")
    soup = BeautifulSoup(r.text, "lxml")

    payload = {
        "category_id": category_id,
        "title_ru": title,
        "title_en": title,
        "auto_translate": "1",
        "currency": "rub",
        "price": int(price) + int(markup),
        "allow_ask_discount": "on",
        "item_origin": "resale",
        "description_html": "<p>55 1 1</p>",
        "_xfRelativeResolver": f"https://lolz.guru/market/item/add?category_id={category_id}",
        "information_html": "<p>2 2</p>",
        "_xfRelativeResolver": f"https://lolz.guru/market/item/add?category_id={category_id}",
        "_xfToken": get_xfToken(),
        "t": "0",
        "_xfConfirm": "1",
        "submit": "Перейти к добавлению товара",
        "_xfRequestUri": f"/market/item/add?category_id={category_id}",
        "_xfNoRedirect": "1",
        "_xfToken": get_xfToken(),
        "_xfResponseType": "json",
    }
    response = ses.post("https://lolz.guru/market/item/add", data=payload)

    soup = BeautifulSoup(response.text, "lxml")
    logger.info(soup)
    chz = str(soup)
    checj = chz.split("market\/")[1].split("\/")[0]
    time.sleep(3)
    data = {
        "login": login,
        "password": password,
        "login_password": f"{login}:{password}",
        "_xfToken": get_xfToken(),
        "random_proxy": "",
        "_xfRequestUri": f"/market/{checj}/goods/add?t=1641318781",
        "_xfNoRedirect": "1",
        "_xfToken": get_xfToken(),
        "_xfResponseType": "json",
    }

    resp = ses.post(
        f"https://lolz.guru/market/{checj}/goods/check", data=data).json()
    logger.success("Выставил аккаунт на продажу")

    data = f"""
    
    👑 Выставил на продажу аккаунт

    info: {login}:{password}
    login: {login}
    password: {password}
    

    👑 Название темы: {title}
    💸 Цена акканута: {price}

    🏆 Аккаунт - https://lolz.guru/market/{checj}


    """
    r = ses.get(
        f"https://api.telegram.org/bot{bot_token}/sendmessage?chat_id={chat_id}&text={data}"
    )


def main():
    ctypes.windll.kernel32.SetConsoleTitleW(
        f" 𝘔𝘢𝘳𝘬𝘦𝘵𝘉𝘰𝘵 | 𝘉𝘢𝘭𝘢𝘯𝘤𝘦: 0 | 𝘗𝘶𝘳𝘤𝘩𝘢𝘴𝘦: 0 ")
    authorization()
    parse()


if __name__ == "__main__":

    main()
# изменить условие баланса
