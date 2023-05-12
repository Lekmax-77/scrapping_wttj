##
## MALEK PROJECT, 2023
## scrapping_wttj
## File description:
## get_date
##

from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime
from datetime import timedelta
import sys
from selenium.webdriver.chrome.options import Options
from class_info import info
from get_info_from_url import get_info_from_url
from send_mail import send_crash


def convert_str_to_delai(date):
    delai = 0
    if date == "24h":
        delai = 1
    elif date == "1 week":
        delai = 7
    elif date == "1 month":
        delai = 30
    elif date == "3 month":
        delai = 90
    else:  # option "all"
        delai = None  # ou un grand nombre de jours pour récupérer toutes les données
    return delai
    

def loop_in_list_of_url(driver, mail, date):
    # this while loop is to scroll down the page to load all the jobs
    list_of_element = []
    nb_next_page = 1
    page = driver.find_elements(By.CLASS_NAME, "sc-dOpmdR")
    nb_page = len(page) - 2
    count = 0 # TODO to delete
    while True:
        for i in range(1, len(driver.find_elements(By.CLASS_NAME, "sc-kZwcoV")) + 1):

            xpath_to_search_one = "/html/body/div[1]/div[1]/div/div/div/div[2]/div/ol/div[" + i.__str__() + "]/li/div/div/div[2]/a"
            try:
                xpath_to_search = "/html/body/div[1]/div[1]/div/div/div/div[2]/div/ol/div[" + i.__str__() +\
                                  "]/li/div/div/div[2]/div[3]/div[1]/p/time"
                result_date = (driver.find_element(By.XPATH, xpath_to_search).get_attribute("datetime").split("T")[0])
                result_url = (driver.find_element(By.XPATH, xpath_to_search_one).get_attribute("href"))
                list_of_element.append((result_url, result_date))

            except Exception as e:
                print("Une erreur s'est produite!(" + e.__str__() + ")\n", file=sys.stderr)
        # input("Appuyez sur entrée pour continuer...")
        nb_next_page += 1
        if nb_next_page > nb_page:
            break
        page[nb_next_page].click()
        sleep(1)
    
    # get the info from the url and put it in a list
    delai = convert_str_to_delai(date)
    date_actuelle = datetime.now()
    date_precedente = None
    if delai is not None:
        date_precedente = date_actuelle - timedelta(days=delai)
    data_of_get_url = []

    for i in range(len(list_of_element)):
        if count == 10:
            break
        print(i.__str__() + "/" + str(len(list_of_element)), file=sys.stderr)
        date_of_job = datetime.strptime(list_of_element[i - 1][1], "%Y-%m-%d")
        if delai is None or date_of_job >= date_precedente:
            try:
                data_of_get_url.append(get_info_from_url(driver, list_of_element[i - 1][0], list_of_element[i - 1][1]))
                print("is append nb " + i.__str__() + "/" + len(list_of_element).__str__(), file=sys.stderr)
                count += 1
            except Exception as e:
                if mail is not None:
                    send_crash(mail, "error in get_info_from_url(" + e.__str__() + ")")
                else:
                    print("Une erreur s'est produite!(" + e.__str__() + ")\n", file=sys.stderr)
                exit(84) 
    return data_of_get_url
    # manage the name of the file
