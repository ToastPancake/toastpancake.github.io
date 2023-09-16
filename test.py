from splinter import Browser
from selenium.webdriver.firefox.service import Service

my_service = Service()
browser = Browser('firefox', service=my_service)
browser.visit('https://chat.openai.com/')
browser.find_by_id('prompt-textarea').fill('In one number, what is the average weight of a human.')
browser.find_by_css('.icon-sm m-1 md:m-0').click()
