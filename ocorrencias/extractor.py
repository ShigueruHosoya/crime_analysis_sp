#%%
import requests
import pandas as pd
import os  
import time
from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import concurrent.futures

def get_browser():
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory' : os.path.join(os.getcwd(),'data')}
    chrome_options.add_experimental_option('prefs', prefs)
    ChromeDriverPath = os.path.join(os.getcwd(),'webdriver','chromedriver.exe')
    
    
    browser = webdriver.Chrome(executable_path=ChromeDriverPath, options=chrome_options)
    url ="http://www.ssp.sp.gov.br/Estatistica/Pesquisa.aspx"

    browser.get(url)
    return browser

def select_capital(browser):
    dropdown_element_region = browser.find_element_by_id("conteudo_ddlRegioes")
    select = Select(dropdown_element_region)

    select.select_by_visible_text("Capital")

def list_year_options(browser):
    dropdown_element_year = browser.find_element_by_id("conteudo_ddlAnos")
    select_year = Select(dropdown_element_year)

    year_options = select_year.options

    return [year_options[value].text for value in range(len(year_options)) if 'Todos' not in year_options[value].text]

def list_all_dps(browser):
    dropdown_element_dps = browser.find_element_by_id("conteudo_ddlDelegacias")
    select_dp = Select(dropdown_element_dps)

    dp_options = select_dp.options

    return [dp_options[value].text for value in range(len(dp_options)) if 'Todos' not in dp_options[value].text]


def select_dp(browser,dp):
    dropdown_element_dps = browser.find_element_by_id("conteudo_ddlDelegacias")
    select = Select(dropdown_element_dps)

    select.select_by_visible_text(r"{}".format(dp))


def select_year(browser,year):
    dropdown_element_year = browser.find_element_by_id("conteudo_ddlAnos")
    select = Select(dropdown_element_year)

    select.select_by_visible_text(year)

def download_csv(browser):
    browser.find_element_by_id("conteudo_btnExcel").click()
#%%

t = get_browser()
select_capital(t)
list_dps = list_all_dps(t)
t.close()
# %%

'''
for dp in list_dps:
        browser_dp = get_browser()
        select_capital(browser_dp)
        select_dp(browser_dp,dp)
        dp_list_years = list_year_options(browser_dp)
        for year in dp_list_years:
            select_year(browser_dp, year)
            download_csv(browser_dp)
        time.sleep(5)
        browser_dp.close()
        '''
def get_dp_info(dp):
    browser_dp = get_browser()
    select_capital(browser_dp)
    select_dp(browser_dp,dp)
    dp_list_years = list_year_options(browser_dp)
    for year in dp_list_years:
        select_year(browser_dp, year)
        download_csv(browser_dp)
    time.sleep(5)
    browser_dp.close()

#%%
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(get_dp_info, list_dps)
# %%
