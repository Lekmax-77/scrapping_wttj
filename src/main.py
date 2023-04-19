import csv
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from datetime import datetime
from datetime import timedelta
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from class_info import info
from get_info_from_url import get_info_from_url
import argparse


def setup_driver(link, headless_mode):
    # setup all driver settings
    s = Service(ChromeDriverManager().install())
    chrome_options = Options()
    if headless_mode == "False":
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=s, options=chrome_options)
    driver.maximize_window()
    driver.get(link)
    sleep(5)
    return driver
    

def manage_arguments():
    # Créer un objet ArgumentParser
    parser = argparse.ArgumentParser(description='Description de votre programme')

    # Ajouter des arguments
    parser.add_argument('-l', '--link', help='url of welcome to the jungle search', required=True)
    parser.add_argument('-n', '--name', help='name of the search', default='nameless')
    parser.add_argument('-d', '--date', default='all' , choices=['24h', '1 week', '1 month', '3 month', "all"], help='date of the job')
    parser.add_argument('-t', '--type', default='json', choices=['json', 'csv'], help='type of the output')
    parser.add_argument('-f', '--format', default='print', choices=['print', 'file'], help='format of the output')
    parser.add_argument('-w', '--headless', default='False', choices=['False', 'True'], help='headless mode (default: False)')
    
    

    # Analyser les arguments
    args = parser.parse_args()
    return args


def main():
    args = manage_arguments()
    link = args.link
    name = args.name
    date = args.date
    format = args.format
    type = args.type
    driver = setup_driver(link, args.headless)
    
    # this while loop is to scroll down the page to load all the jobs
    list_of_url = []
    list_of_date_of_url = []
    y = 0
    while True:
        for i in range(1, len(driver.find_elements(By.CLASS_NAME, "sc-1peil1v-5")) + 1):
            xpath_to_search_one = "/html/body/div[1]/div[1]/div/div/div/div/div/div[3]/div/ol/div[" + i.__str__() + "]/li/article/div[1]/a"
            try:
                xpath_to_index_liste = "/html/body/div[1]/div[1]/div/div/div/div/div/div[3]/div/ol/div[" + i.__str__() + "]/li/article/div[2]/header/ul"
                index_to_liste = (len(driver.find_element(By.XPATH, xpath_to_index_liste).find_elements(By.TAG_NAME, "li")) - 0).__str__()
                xpath_to_search = "/html/body/div[1]/div[1]/div/div/div/div/div/div[3]/div/ol/div[" + i.__str__() + "]/li/article/div[2]/header/ul/li[" + index_to_liste  + "]/span[2]/time"
                list_of_date_of_url.append(driver.find_element(By.XPATH, xpath_to_search).get_attribute("datetime").split("T")[0])# .find_element(By.TAG_NAME, "time").
                list_of_url.append(driver.find_element(By.XPATH, xpath_to_search_one).get_attribute("href"))
            except Exception as e:
                print("Une erreur s'est produite!(" + e.__str__() + ")\n", file=sys.stderr)
        if y >= (len(driver.find_elements(By.CLASS_NAME, "sc-bwsPYA")) - 3):
            break
        driver.find_elements(By.CLASS_NAME, "sc-bwsPYA")[len(driver.find_elements(By.CLASS_NAME, "sc-bwsPYA"))- 1].click()
        sleep(1)
    # check if the list of url and the list of date are the same size
    if len(list_of_url) != len(list_of_date_of_url):
        print("error", file=sys.stderr)
        exit(84)
        
        
    # get the info from the url and put it in a list
    delai = 0
    if date == "24h":
        delai = 1
    elif date == "1 semaine":
        delai = 7
    elif date == "1 mois":
        delai = 30
    elif date == "3 mois":
        delai = 90
    else:  # option "all"
        delai = None  # ou un grand nombre de jours pour récupérer toutes les données
    date_actuelle = datetime.now()
    print(date_actuelle, file=sys.stderr)
    if delai is not None:
        date_precedente = date_actuelle - timedelta(days=delai)
    data_of_get_url = []
    for i in range(len(list_of_url)):
        print(i.__str__() + "/" + str(len(list_of_url)) , file=sys.stderr)
        date_of_job = datetime.strptime(list_of_date_of_url[i - 1], "%Y-%m-%d")
        if delai is None or date_of_job >= date_precedente:
            data_of_get_url.append(get_info_from_url(driver, list_of_url[i], list_of_date_of_url[i - 1]))

    
    # manage the name of the file
    name_of_the_file = "scrappin_data_of_wttj_" + name + "_of_" + date + "_" + datetime.now().strftime("%d-%m-%Y-%H-%M")
    
    # manage the output
    if type == "json":
        data = {"job": [p.__dict__ for p in data_of_get_url]}
        if format == "print":
            json_str = json.dumps(data)
            print(json_str)
        elif format == "file":
            with open(name_of_the_file + ".json", 'w') as f:
                json.dump(data, f)
    elif type == "csv":
        if format == "print":
            print(";".join(info.__dict__.keys()))
            for p in data_of_get_url:
                print(";".join(p.__dict__.values()))
        elif format == "file":
            with open(name_of_the_file + ".csv", 'w') as f:
                writer = csv.writer(f)
                writer.writerow(info.__dict__.keys())
                for p in data_of_get_url:
                    writer.writerow(p.__dict__.values())

if __name__ == '__main__':
    main()
