#
# EPITECH PROJECT, 2023
# scrapping_wttj
# File description:
# new_gui.py
#


import tkinter as tk
from tkinter import ttk, filedialog
import csv
import json
from datetime import datetime
from setup_driver import setup_driver
from get_data import loop_in_list_of_url


def read_csv_file(file_path):
    urls = []
    names = []

    with open(file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        print(reader.fieldnames)
        input("wait")
        for row in reader:
            url = row['Url']
            name = row['Name']
            urls.append(url)
            names.append(name)
    return urls, names


class Data:
    def __init__(self, file_path, file_format, duration):
        self.file_path = file_path
        self.file_format = file_format
        self.duration = duration


class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("400x300")  # Dimension de la fenêtre
        self.window.title("Mon GUI")
        self.data = None  # Variable pour stocker les données
        self.create_widgets()
        # self.file_entry = None
        # self.format_combobox = None
        # self.duration_combobox = None

    def create_widgets(self):
        # Création de la frame principale
        frame = ttk.Frame(self.window, padding="20")
        frame.grid(column=0, row=0, sticky="nsew")
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        # Création du bouton de parcourir pour l'explorateur de fichiers
        browse_button = ttk.Button(frame, text="Parcourir", command=self.browse_file)
        browse_button.grid(column=0, row=0, sticky="w")

        # Création de la zone de sélection du fichier
        self.file_entry = ttk.Entry(frame, width=30)
        self.file_entry.grid(column=1, row=0)

        # Création du menu déroulant pour le format de fichier
        format_label = ttk.Label(frame, text="Format de fichier:")
        format_label.grid(column=0, row=1, sticky="w")
        self.format_combobox = ttk.Combobox(frame, values=["csv", "json"], state="readonly")
        self.format_combobox.grid(column=1, row=1)
        self.format_combobox.current(0)  # Sélectionne le premier élément par défaut

        # Création du menu déroulant pour la durée
        duration_label = ttk.Label(frame, text="Durée:")
        duration_label.grid(column=0, row=2, sticky="w")
        self.duration_combobox = ttk.Combobox(frame, values=["24h", "1 week", "1 month", "3 months", "all"],
                                              state="readonly")
        self.duration_combobox.grid(column=1, row=2)
        self.duration_combobox.current(0)  # Sélectionne le premier élément par défaut

        # Création du bouton de validation
        submit_button = ttk.Button(frame, text="Valider", command=self.submit)
        submit_button.grid(column=1, row=3, pady=10)

    def browse_file(self):
        filetypes = (("Tous les fichiers", "*.*"), ("Fichiers Excel", "*.xls;*.xlsx;*.csv"))
        file_path = filedialog.askopenfilename(title="Sélectionnez un fichier", filetypes=filetypes)
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, file_path)

    def submit(self):
        file_path = self.file_entry.get()
        file_format = self.format_combobox.get()
        duration = self.duration_combobox.get()

        if file_path:
            # Stocker les informations dans la classe Data
            self.data = Data(file_path, file_format, duration)
            self.window.destroy()


def main():
    gui = GUI()
    gui.window.mainloop()

    # Récupérer les données après la fermeture de la fenêtre
    if gui.data:
        print("Informations récupérées :")
        print("Chemin du fichier :", gui.data.file_path)
        print("Format de fichier :", gui.data.file_format)
        print("Durée :", gui.data.duration)

        urls, names = read_csv_file(gui.data.file_path)
        for url, name in zip(urls, names):
            name_of_the_file = "scrappin_data_of_wttj_" + name + "_of_" + gui.data.duration + "_" + \
                               datetime.now().strftime("%d-%m-%Y-%H-%M")
            driver = setup_driver(url, False)
            # loop in the list of url
            data_of_get_url = loop_in_list_of_url(driver, None, gui.data.duration)
            # manage the output

            if gui.data.file_format == "json":
                data = {"job": [p.__dict__ for p in data_of_get_url]}
                with open(name_of_the_file + ".json", 'w') as f:
                    json.dump(data, f)
            elif gui.data.file_format == "csv":
                with open(name_of_the_file + ".csv", 'w') as f:
                    writer = csv.writer(f)
                    writer.writerow(data_of_get_url[0].get_name_of_all_attributes())
                    for p in data_of_get_url:
                        writer.writerow(p.get_list())
        return 0


if __name__ == "__main__":
    main()
