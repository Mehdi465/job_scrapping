import requests
from bs4 import BeautifulSoup
import pandas as pd
from enum import Enum
from job_offer import JobOffer

# this class contains all infos about a job offer that i care
class JobOffer:

    def __init__(self,job_name,company_name,link,location,salary,id) -> None:
        self.job_name = job_name
        self.company_name = company_name
        self.link = link
        self.location = location
        self.salary = salary
        self.id = id



class JobWebSite(Enum):
    All = 0
    Linkedin = 1
    Indeed = 2

# This class aims to Scrap jobs offer on different site
class JobScrapper:
    def __init__(self,job_title:str,location:str,website:JobWebSite):
        self.job_title = job_title   # for example : software engineer
        self.location = location     # location (city, or country): Toronto, Japan etc...
        self.website = website       # website selected : see JobWebSite class

    def get_job_offer_linkeding(self):
        url = f"https://www.linkedin.com/jobs/search/?currentJobId=4010735510&keywords={self.job_title}&location={self.location}&origin=JOBS_HOME_SEARCH_BUTTON&refresh=true"
        response = requests.get(url)

        return response

    def get_job_offer_indeed(self):
        pass

    def get_job_offer(self):
        """use GET request to the selected site.
        :return: [response] of request"""

        if self.website == JobWebSite.All:
            response_linkedin = JobScrapper.get_job_offer_linkeding()
            response_indeed = JobScrapper.get_job_offer_indeed()

            return [response_linkedin,response_indeed]

        elif self.website == JobWebSite.Linkedin:
            response_linkedin = JobScrapper.get_job_offer_linkeding()

            return [response_linkedin]

        elif self.website == JobWebSite.Indeed:
            response_indeed = JobScrapper.get_job_offer_indeed()

            return [response_indeed]

    def extract_jobs_infos(self,response) -> list(JobOffer):
        ## request succeded
        if (response.status_code == 200):
            pass

        else:
            print("Response")




job_title = "software engineer"
job_title = job_title.replace(" ","%20")
location = "Toronto"

list_url = f"https://www.linkedin.com/jobs/search/?currentJobId=4010735510&keywords={job_title}&location={location}&origin=JOBS_HOME_SEARCH_BUTTON&refresh=true"

job_id = 3901532998

job_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"

response = requests.get(list_url)
print(response.status_code == 200)


#with open("file.html","w+") as file_:
#    file_.write(response.text)
