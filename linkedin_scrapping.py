import requests
from bs4 import BeautifulSoup
import pandas as pd
from enum import Enum
from job_offer import JobOffer
import folium
from geopy.geocoders import Nominatim
import requests
import pandas
import branca

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

    def extract_city_from_location(self):
        return self.location.split(",")[0].strip()   

    def get_city_coordinates_from_name(self):
        location = None
        geolocator = Nominatim(user_agent="geoapiExecises")
        location = geolocator.geocode(JobOffer.extract_city_from_location(self.location))

        if location:
            return location
        else:
            print("City not found")
            return None    

    def create_marker(self):
        # get location in Earth format
        location_xy = JobOffer.get_city_coordinates_from_name()

        html = f"""
        <h1> {self.job_name}</h1><br>
        {self.company_name}
        <p>
        <code>
            {self.link}
        </code>
        <code>
            {self.website}
        </code>
        </p>
        """

        iframe = branca.element.IFrame(html=html, width=500, height=300)
        popup1 = folium.Popup(iframe, max_width=500)

        #create the Marker
        marker = folium.Marker(
            location=[location_xy.latitude, location_xy.longitude],
            tooltip=f"{self.job_name}",
            popup=popup1,
            icon=folium.Icon(icon="cloud"),
        )

        return marker

# stores reponses to analyze them
class Response:
    def __init__(self,website : JobWebSite, content) -> None:
        self.site = website
        self.content = content

    def request_succeeded(self):
        return self.content.status_code == 200

    def get_info_one_job(html_part_job,soup) -> JobOffer:
        """for one job in the page, extract all related info"""

        # Parse the HTML
        #soup = BeautifulSoup(html_part_job, 'html.parser')
        # Extract job ID from the 'data-entity-urn' attribute
        job_id = soup.find('div', class_='job-search-card')['data-entity-urn'].split(':')[-1]
        # Extract job link from the 'href' attribute
        job_link = soup.find('a', class_='base-card__full-link')['href']
        # Extract job name
        job_name = soup.find('h3', class_='base-search-card__title').text.strip()
        # Extract company name
        company_name = soup.find('h4', class_='base-search-card__subtitle').text.strip()
        # Extract job location
        location = soup.find('span', class_='job-search-card__location').text.strip()

        job_result = JobOffer(job_name,company_name,job_link,location,salary=None,id=job_id,website=None)

        return job_result


    def get_all_job(self) -> list[JobOffer]:
        """Parse the text in reponse"""
        jobs = []
        # Parse the HTML
        soup = BeautifulSoup(self.content.text, 'html.parser')
        # Find all job cards using the class pattern
        job_cards = soup.find_all('div', class_="base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card")

        for job_card in job_cards:
            jobs.append(Response.get_info_one_job(job_card,soup))

        return jobs

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
            response_linkedin = self.get_job_offer_on_website(JobWebSite.Linkedin)
            response_indeed = self.get_job_offer_on_website(JobWebSite.Indeed)

            responses_researches = [response_linkedin,response_indeed]

        else:
            for website in self.websites:
                responses_researches.append(self.get_job_offer_on_website(website))

        return responses_researches

    def extract_jobs_infos(responses:list[Response]) -> list[JobOffer]:

        list_jobs = []

        for response in responses:
            # if response succed
            if response.request_succeeded():
                list_jobs += response.get_all_job()

            # else inform user that this request did not succeed
            else:
                print(f"request for research on {response.site} did not succeeded with status code : {response.content.status_code}")

        return list_jobs

####################################
###-------------MAIN-------------###
####################################

def mock_response():
    """mock the response to the get job request"""
    content = ""
    with open("results/file.html","r+") as html_file:
        content = html_file.read()

    return Response(JobWebSite.Linkedin,content)

if __name__ == "__main__":
    # INPUTS
    job_title = "software engineer"
    job_title = job_title.replace(" ","%20") # in url request " " is replaced by "%20"
    location = "Toronto"
    sites = [JobWebSite.Linkedin]


    # create the variable to make the get request
    job_research = JobScrapper(job_title,
                               location,
                               websites=sites)
    # do the request
    all_responses = job_research.get_job_offer()

    # get all jobs and their infos 
    all_jobs = JobScrapper.extract_jobs_infos(all_responses)

    ### ------------- MAP PART --------------- ###

    #################################################
    ### ------------- TESTING PART -------------- ###
    #################################################

    m = folium.Map(tiles="CartoDB Voyager")

    for job in all_jobs:
        # create marker and add it to the map
        job.create_marker().add_to(m)


        m.save("results/index.html")    
        input("ok")


    TEST=False
    if TEST:
        test_url = f"https://www.linkedin.com/jobs/search?&keywords={job_title}&location={location}&original_referer=https%3A%2F%2Fwww.linkedin.com%2Fjobs%2Fsearch%3Fkeywords%3Dsoftware%2520engineer%26location%3DCanada&position=1"
        list_url = f"https://www.linkedin.com/jobs/search?&keywords={job_title}&location={location}&origin=JOBS_HOME_SEARCH_BUTTON&refresh=true"

        job_id = 4008212439

        job_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"

        response = requests.get(test_url)
        print(response.status_code == 200)

        with open("results/file.html","w+",encoding="utf-8") as file_:
            file_.write(response.text)
