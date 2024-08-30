import requests
from bs4 import BeautifulSoup
import pandas as pd


job_title = "software engineer"
job_title = job_title.replace(" ","%20")
location = "Toronto"

list_url = f"https://www.linkedin.com/jobs/search/?currentJobId=4010735510&keywords={job_title}&location={location}&origin=JOBS_HOME_SEARCH_BUTTON&refresh=true"

job_id = 3901532998

job_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"

response = requests.get(job_url)
print(response)




with open("file.html","w+") as file_:
    file_.write(response.text)
