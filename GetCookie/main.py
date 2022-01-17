import time
import pickle
import logger
from selenium import webdriver
from loguru import logger

driver = webdriver.Chrome()
driver.get("https://lolz.guru")
logger.success("Нажмите ENTER в консоле когда закончите входить в ваш аккаунт")
input("Нажмите ENTER когда войдете в ваш аккаунт")
pickle.dump(driver.get_cookies(), open("session", "wb"))