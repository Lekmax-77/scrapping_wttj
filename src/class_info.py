##
## MALEK PROJECT, 2023
## scrapping_wttj
## File description:
## class_info
##

class info:
    
    def __init__(self, url):
        self.job_link = url
        self.job_name= "None"
        self.job_contract= "None"
        self.job_location= "None"
        self.job_categories = "todo"
        self.job_published_at = "todo"
        self.job_description= "None"
        self.job_level= "None"
        self.company_name= "None"
        self.company_domain= "None"
        self.company_linkedin_url= "None"
        self.company_industry= "None"
        self.company_staff_count= "None"
        self.company_tools= "None"
        self.company_address= "None"
        self.company_labels = "todo"
        self.company_description= "None"
        self.company_logo= "None"


    def get_list(self):
        return  [self.job_link,
                 self.job_name , 
                 self.job_contract ,
                 self.job_location , 
                 self.job_categories ,
                 self.job_published_at, 
                 ' '.join(self.job_description.split("\n")) ,
                 self.job_level ,
                 self.company_name , 
                 self.company_domain ,
                 self.company_linkedin_url  ,
                 self.company_industry , 
                 self.company_staff_count ,
                 ' '.join(self.company_tools.split('\n')) , 
                 self.company_address , 
                 self.company_labels , 
                 ' '.join(self.company_description.split("\n")), 
                 self.company_logo]



    def __str__(self):
        return  self.job_link + "\n" + self.job_name + "\n" + self.job_contract + "\n" + self.job_location + "\n" + self.job_categories + "\n" + self.job_published_at + ';' + ' '.join(self.job_description.split("\j")) + "\n" + self.job_level + "\n" + self.company_name + "\n" + self.company_domain + "\n" + self.company_linkedin_url  + "\n" + self.company_industry + "\n" + self.company_staff_count + "\n" + ' '.join(self.company_tools.split('\n')) + "\n" + self.company_address + "\n" + self.company_labels + "\n" + ' '.join(self.company_description.split("\j"))+ "\n" + self.company_logo
