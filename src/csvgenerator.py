import csv

def write_csv_file(file_path, urls, names):
    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(['Url', 'Name'])  # Écriture de l'en-tête
        for url, name in zip(urls, names):
            writer.writerow([url, name])  # Écriture des lignes

# Exemple d'utilisation
file_path = '/home/lekmax_77/PROJECT/FREELANCE/Gemna/scrapping_wttj/fichier.csv'
urls = ['https://www.welcometothejungle.com/fr/jobs?query=devops&page=1&searchTitle=true&refinementList%5Borganization.size.fr%5D%5B%5D=%3C%2015%20salari%C3%A9s&refinementList%5Borganization.size.fr%5D%5B%5D=Entre%2015%20et%2050%20salari%C3%A9s&refinementList%5Borganization.size.fr%5D%5B%5D=Entre%2050%20et%20250%20salari%C3%A9s&refinementList%5Borganization.size.fr%5D%5B%5D=Entre%20250%20et%202000%20salari%C3%A9s&refinementList%5Bprofession_name.fr.Tech%5D%5B%5D=DevOps%20%2F%20Infra&refinementList%5Bprofession_name.fr.Tech%5D%5B%5D=S%C3%A9curit%C3%A9']
names = ['Devops']

write_csv_file(file_path, urls, names)