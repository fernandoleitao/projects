import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains


service = Service('/home/fernando/Projects/teste_selenium/chromedriver')
service.start()
driver = webdriver.Remote(service.service_url)
action_chains = ActionChains(driver)
driver.get('http://web.trf3.jus.br/certidao/Certidao/Solicitar')
driver.find_element_by_xpath('//input[@id="abrangenciaSJSP"]').click()
driver.find_element_by_xpath('//input[@id="Nome"]').send_keys('Fernando Nunes José Leitão')
driver.find_element_by_xpath('//input[@id="CpfCnpj"]').click()
driver.find_element_by_xpath('//input[@id="CpfCnpj"]').send_keys('35959049821')
src = driver.find_element_by_xpath('//img[@id="ImagemCaptcha"]')
action_chains.move_to_element(src).context_click().send_keys(Keys.SHIFT, Keys.ARROW_DOWN).send_keys(Keys.SHIFT, Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()
sleep(3)