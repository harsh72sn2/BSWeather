import json
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
import requests

data12 = open('City.json')
data123 = json.load(data12)
city = data123["City"]
v = data123["Variance"]
VarianceCheck = {}
temperatureAPI = []
temperatureWeb = []
data12.close()

for ct in city:
    url = "http://api.openweathermap.org/data/2.5/weather?q=" + ct + "&appid=29e82763001bc04ba7a07d2bf13ea2aa"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    rsp = response.json()
    maindata = rsp.get('main')
    temp1 = maindata["temp"] - 273.15
    temperatureAPI.append(maindata["temp"])

    driver = webdriver.Chrome("C:\\Users\\harsh\\Downloads\\chromedriver\\chromedriver.exe")
    wait = WebDriverWait(driver, 40)
    driver.maximize_window()
    driver.get("https://weather.com/")
    attempts = 0
    while attempts < 2:
        try:
            search = wait.until(ec.element_to_be_clickable((By.ID, "LocationSearch_input")))
            search.send_keys(ct)
            searchcl = wait.until(ec.element_to_be_clickable((By.ID, "LocationSearch_listbox-0")))
            searchcl.click()
            t2 = driver.find_element_by_xpath("//span[@class='CurrentConditions--tempValue--3KcTQ']").text
            temperatureWeb.append(t2)
            temp2 = t2.rstrip("°")
            result = True
            break
        except StaleElementReferenceException:
            if attempts == 2:
                raise
            attempts += 1

    check = float(temp2) - temp1
    if check == v:
        VarianceCheck[ct] = "Not Greater than variance"
    else:
        VarianceCheck[ct] = "Greater than Variance"
    driver.quit()

print("Temperature Web:")
print(temperatureWeb)
print()
print("Temperature API:")
print(temperatureAPI)
print()
print("Variance Check:")
print(VarianceCheck)

