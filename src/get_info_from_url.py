#
# MALEK PROJECT, 2023
# scrapping_wttj
# File description:
# get_info_from_url
#

from selenium.webdriver.common.by import By
from time import sleep
from class_info import info


def get_info_from_url(driver, url, date) -> info:
    
    driver.get(url)
    sleep(1)
    _info = info(url)
    _info.job_published_at = date
    _info.job_name = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/div/main/div[1]/div/div/h1").text
    try:
        _info.job_location = driver.find_element(
            By.XPATH, "/html/body/div[1]/div[1]/div/div/div/main/div[1]/div/div/li/span[2]/a/span").text
    except:
        pass
    # elements = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/div/main/div[1]/div/div/div"
    #                                ).find_elements(By.CLASS_NAME, "ljsr3q-0 ")
    elements = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/div/main/div[1]/div/div/div"
                                   )
    for uno in elements.find_elements(By.TAG_NAME, "i"):
        print("go")
        try:
            _info.job_contract = uno.find_element(By.NAME, "contract").text
            print("work contract")
        except:
            pass
        print("next")
        try:
            _info.job_level = uno.find_element(By.NAME, "education_level").text
            print("work level")
        except:
            pass
        print("end")
    _info.job_description = driver.find_element(By.ID, "description-section").text
    _info.company_name = driver.find_element(By.XPATH,
                                             "/html/body/div[1]/div[1]/div/div/div/main/div[1]/div/div/a/span").text
    _info.company_logo = driver.find_element(By.XPATH,
                                             "/html/body/div[1]/div[1]/div/div/div/main/div[1]/div/div/a/div/figure/img").get_attribute("src")
    _info.company_description = driver.find_element(By.ID, "about-section").text
    driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/div/main/div[1]/div/div/a").click()
    sleep(1)
    try:
        _info.company_staff_count = driver.find_element(By.XPATH,
                                                        "/html/body/div[1]/div[1]/div/div/div/main/div/div/section/div[1]/div[1]/div/div[4]/div/div/article/div/ul/li[2]/span").text
    except:
        pass
    for one in driver.find_elements(By.CLASS_NAME, "k2ldby-0"):
        try:
            one.find_element(By.NAME, "earth")
            _info.company_domain = one.find_elements(By.TAG_NAME, "span")[1].find_element(By.TAG_NAME, "a").get_attribute("href")
            break
        except:
            pass
    try:

        tempo_2 = driver.find_element(By.CLASS_NAME, "sc-16kqxrj-4").find_elements(By.TAG_NAME, "a")
        for one in tempo_2:
            if "linkedin" in one.get_attribute("href"):
                _info.company_linkedin_url = one.get_attribute("href")
                break
    except:
        _info.company_linkedin_url= "None"
    _info.company_industry = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/div/main/section/div/header/div/ul/li[1]/span[2]").text
    _info.company_address = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/div/main/section/div/header/div/ul/li[2]/span[2]").text
    save_url = driver.current_url
    driver.get(driver.current_url + "/tech")
    sleep(0.5)
    temps = driver.find_elements(By.CLASS_NAME, "f9afj1-0")
    for one in temps:
        _info.company_tools += one.text
        if one != temps[-1]:
            _info.company_tools += ", "
    driver.get(save_url + "/jobs")
    sleep(0.5)
    all_jobs = driver.find_elements(By.CLASS_NAME, "sc-1peil1v-4")
    for one in all_jobs:
        _info.company_jobs += one.text
        if one != all_jobs[-1]:
            _info.company_jobs += ", "
    _info.company_nb_of_jobs = len(all_jobs)

    return _info

