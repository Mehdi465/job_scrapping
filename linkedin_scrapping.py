import requests
from bs4 import BeautifulSoup
import pandas as pd
from enum import Enum
from job_offer import JobOffer

#Contains all websites for the research
class JobWebSite(Enum):
    All = 0
    Linkedin = 1
    Indeed = 2

# this class contains all infos about a job offer that I care
class JobOffer:
    def __init__(self,job_name:str,company_name:str,link:str,location:str,salary:str,id:str,website:JobWebSite) -> None:
        self.job_name = job_name
        self.company_name = company_name
        self.link = link
        self.location = location
        self.salary = salary
        self.id = id
        self.website = website

# stores reponses to analyze them
class Response:
    def __init__(self,website : JobWebSite, content) -> None:
        self.site = website
        self.content = content

    def request_succeeded(self):
        return self.response.status_code == 200

    def get_info_one_job(self) -> JobOffer:
        """for all jobs in the page, extract """
        job_name = None
        company_name = None
        link = None
        location = None
        salary = None
        id = None
        website = None

        pass

    def get_all_job(self) -> list[JobOffer]:
        """Parse the text in reponse"""
        pass

# This class aims to Scrap jobs offer on different site
class JobScrapper:
    def __init__(self,job_title:str,location:str,websites:list[JobWebSite]):
        self.job_title = job_title   # for example : software engineer
        self.location = location     # location (city, or country): Toronto, Japan etc...
        self.websites = websites

    def get_job_offer_on_website(self,website:JobWebSite) -> Response:

        website_url = ""
        match (website):
            case JobWebSite.Linkedin:
                website_url = f"https://www.linkedin.com/jobs/search?keywords={self.job_title}&location={self.location}"
            case JobWebSite.Indeed:
                #TODO
                website_url = ""

        response = Response(JobWebSite.Linkedin, requests.get(website_url))
        print(f"research sent to {website}")

        return response

    def get_job_offer(self):
        """use GET request to the selected site.
        :return: list[response] of request"""

        responses_researches = []

        if self.websites == JobWebSite.All:
            response_linkedin = Response(JobWebSite.Linkedin, JobScrapper.get_job_offer_on_website(JobWebSite.Linkedin))
            response_indeed = Response(JobWebSite.Indeed, JobScrapper.get_job_offer_on_website(JobWebSite.Indeed))

            responses_researches = [response_linkedin,response_indeed]

        else:
            for website in self.websites:
                responses_researches.append(Response(website,website))

        return responses_researches

    def extract_jobs_infos(responses:list[Response]) -> list[JobOffer]:

        list_jobs = []

        for response in responses:
            # if response succed
            if response.request_succeeded():
                list_jobs += response.get_all_job()

            # else inform user that this request did not succeed
            else:
                print(f"request for research on {response.site} did not succeeded with response code {response.content.text}")

        return list_jobs

####################################
###-------------MAIN-------------###
####################################

if __name__ == "__main__":
    # INPUTS
    job_title = "software engineer"
    job_title = job_title.replace(" ","%20") # in url request " " is replaced by "%20"
    location = "Toronto"
    sites = [JobWebSite.Linkedin]
    """

    # create the variable the make the get request
    job_research = JobScrapper(job_title,
                               location,
                               websites=sites)
    # do the request
    all_responses = job_research.get_job_offer()

    print(all_responses) """

    #all_jobs = JobScrapper.extract_jobs_infos(all_responses)

    #################################################
    ### ------------- TESTING PART -------------- ###
    #################################################

    TEST=True
    if TEST:
        test_url = f"https://www.linkedin.com/jobs/search?&keywords={job_title}&location={location}&original_referer=https%3A%2F%2Fwww.linkedin.com%2Fjobs%2Fsearch%3Fkeywords%3Dsoftware%2520engineer%26location%3DCanada&position=1"
        list_url = f"https://www.linkedin.com/jobs/search?&keywords={job_title}&location={location}&origin=JOBS_HOME_SEARCH_BUTTON&refresh=true"

        job_id = 4008212439

        job_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"

        response = requests.get(test_url)
        print(response.status_code == 200)

        with open("results/file.html","w+",encoding="utf-8") as file_:
            file_.write(response.text)
