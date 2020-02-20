from selenium import webdriver

browser = webdriver.Chrome()
browser.get('http://quote.eastmoney.com/sh600109.html')
print(browser.page_source)