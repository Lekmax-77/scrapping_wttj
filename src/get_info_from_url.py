##
## MALEK PROJECT, 2023
## scrapping_wttj
## File description:
## get_info_from_url
##

from selenium.webdriver.common.by import By
from time import sleep
from class_info import info

def get_info_from_url(driver, url, date) -> info:
    
    driver.get(url)
    sleep(1)
    _info = info(url)
    _info.job_published_at = date
    _info.job_name = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/div/div/main/section/div/h1").text
    _info.job_contract = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/div/div/main/section/div/ul/li[1]/span[2]/span").text
    for one in driver.find_elements(By.CLASS_NAME, "sc-16yjgsd-0"):
        try:
            one.find_element(By.NAME, "location")
            _info.job_location = one.find_element(By.CLASS_NAME, "wui-text").text
        except:
            pass
        try:
            one.find_element(By.NAME, "education_level")
            _info.job_level = one.find_elements(By.TAG_NAME, "span")[3].text
        except:
            pass
    _info.job_description = driver.find_element(By.ID, "description-section").text
    _info.company_name = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/div/div/main/div[1]/div/div/div[1]/div[1]/a/h4").text
    _info.company_logo = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/div/div/main/section/div/a/div/figure/img").get_attribute("src")
    _info.company_staff_count = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/div/div/main/div[1]/div/div/div[1]/div[1]/ul/li[2]/span[2]").text
    _info.company_description = driver.find_element(By.ID, "about-section").text
    driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/div/div/main/section/div/a").click()
    sleep(1)
    for one in driver.find_elements(By.CLASS_NAME, "sc-16yjgsd-0"):
        try:
            one.find_element(By.NAME, "earth")
            _info.company_domain = one.find_elements(By.TAG_NAME, "span")[1].find_element(By.TAG_NAME, "a").get_attribute("href")
            break
        except:
            pass
    try:

        tempo_2 = driver.find_element(By.CLASS_NAME, "sc-1j9pq7a-4").find_elements(By.TAG_NAME, "a")
        for one in tempo_2:
            if "linkedin" in one.get_attribute("href"):
                _info.company_linkedin_url = one.get_attribute("href")
                break
    except:
        _info.company_linkedin_url= "None"
    _info.company_industry = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/div/main/section/div/header/div/ul/li[1]/span[2]").text
    _info.company_address = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/div/main/section/div/header/div/ul/li[2]/span[2]").text
    driver.get(driver.current_url + "/tech-1")
    sleep(0.5)
    temps = driver.find_elements(By.CLASS_NAME, "sc-17029wj-4")
    for one in temps:
        _info.company_tools += one.text
        if one != temps[-1]:
            _info.company_tools += ", "
    return _info

