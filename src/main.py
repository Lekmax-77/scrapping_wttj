##
## MALEK PROJECT, 2023
## scrapping_wttj
## File description:
## main
##

import csv
import json
from selenium import webdriver
from time import sleep
from datetime import datetime
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import argparse
from get_data import loop_in_list_of_url


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
    parser.add_argument('-w', '--windowless', default='False', choices=['False', 'True'], help='window mode (default: False)')
    parser.add_argument('-m', '--mail',  help='the mail will receive the crash status of the bot')
    
    # Analyser les arguments
    args = parser.parse_args()
    return args


def main():
    # manage the arguments 
    args = manage_arguments()
    
    # setup the driver
    driver = setup_driver(args.link, args.windowless)

    # name of the file
    name_of_the_file = "scrappin_data_of_wttj_" + args.name + "_of_" + args.date + "_" + datetime.now().strftime("%d-%m-%Y-%H-%M")
    
    if not args.mail:
        args.mail = None
    # loop in the list of url
    data_of_get_url = loop_in_list_of_url(driver, args.mail, args.date)
    
    # manage the output
    if args.type == "json":
        data = {"job": [p.__dict__ for p in data_of_get_url]}
        if args.format == "print":
            json_str = json.dumps(data)
            print(json_str)
        elif args.format == "file":
            with open(name_of_the_file + ".json", 'w') as f:
                json.dump(data, f)
    elif args.type == "csv":
        if args.format == "print":
            print(";".join(data_of_get_url[0].get_name_of_all_attributes()))
            for p in data_of_get_url:
                print(";".join(p.get_list()))
        elif args.format == "file":
            with open(name_of_the_file + ".csv", 'w') as f:
                writer = csv.writer(f)
                writer.writerow(data_of_get_url[0].get_name_of_all_attributes())
                for p in data_of_get_url:
                    writer.writerow(p.get_list())


if __name__ == '__main__':
    main()
