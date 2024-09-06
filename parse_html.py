from bs4 import BeautifulSoup

from bs4 import BeautifulSoup

# Sample HTML (you would load your actual HTML file instead)
html_content = ''''''
with open("results/file.html","r+",encoding="utf-8") as html_file:
    html_content = html_file.read()


# Parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Find all job cards using the class pattern
job_cards = soup.find_all('div', class_="base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card")

# List to store job data
jobs = []

# Loop through each job card and extract the data
for card in job_cards:
    # Extract job ID from the 'data-entity-urn' attribute
    input(card)
    job_id = card['data-entity-urn'].split(':')[-1]

    # Extract job link
    job_link = card.find('a', class_='base-card__full-link')['href']

    # Extract job name
    job_name = card.find('h3', class_='base-search-card__title').text.strip()

    # Extract company name
    company_name = card.find('h4', class_='base-search-card__subtitle').text.strip()

    # Extract location
    location = card.find('span', class_='job-search-card__location').text.strip()

    # Store the data in a dictionary
    job_data = {
        'Job ID': job_id,
        'Job Name': job_name,
        'Company Name': company_name,
        'Job Link': job_link,
        'Location': location
    }

    # Add the job data to the list
    jobs.append(job_data)

# Print all the extracted jobs
for job in jobs:
    print(job)
    input("ok")