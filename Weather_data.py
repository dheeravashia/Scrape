from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as WDW
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import sys

def get_weather_data(areacode):

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.get("https://nowdata.rcc-acis.org/"+areacode)
    
    product = WDW(driver,10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div[4]/label[3]/input')))
    product.click()
    start_year = WDW(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="year_area"]/fieldset/input[1]')))
    start_year.clear()
    start_year.send_keys("1900")
    
    end_year = WDW(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="year_area"]/fieldset/input[2]')))
    end_year.clear()
    end_year.send_keys("2024")
    
    clicks = WDW(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="description"]'))).click()
    
    
    go = WDW(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="go"]')))
    go.click()
    time.sleep(10)
    html = driver.page_source
    driver.quit()
    
    soup = bs(html,'html.parser')
    table = soup.find('table', class_="tablesorter tablesorter-default")
    all_rows = table.find_all('tr')[1:-3]
    
    
    varnames = ['date', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Annual']
    df = pd.DataFrame()
    for year in all_rows:
        data_dict = {}
        year_data = year.find_all('td')
        for i, col in enumerate(year_data):
            data_dict[varnames[i]] = col.text
        
        # Create DataFrame from data_dict
        temp_df = pd.DataFrame([data_dict])
        
        # Concatenate temp_df to df
        df = pd.concat([df, temp_df], ignore_index=True)
    
    # Reset the index of df
    df.reset_index(drop=True, inplace=True)
    
    df.to_csv(f"{areacode}_weatherdata.csv", index=False)
    
    
    return

if len(sys.argv) > 1:
    areacode = sys.argv[1]
    get_weather_data(areacode)
else:
    print("Error (Invalid Area Code)")
