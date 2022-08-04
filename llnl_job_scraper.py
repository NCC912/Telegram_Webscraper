# Goal: Fetch URLS for job postings based on user's 
#1. Get 

# Return list
from pprint import PrettyPrinter
from typing import Optional
import requests
from bs4 import BeautifulSoup
import re


url = "https://www.llnl.gov/join-our-team/careers/find-your-job"

def getLLNLJob(skillset: list) -> Optional[list]:
    """Based on a candidates's skillset and preferences, returns ideal jobs 

    Args:
        skillset (list): A list of keywords including skills.

    Returns:
        Optional[list]: Can return a dictionary or nothing if no jobs match the candidate.
    """
    try:
        r = requests.get(url)
    except:
        print("Error occurred retrieving web page contents...")
        return
    else: 
        soup = BeautifulSoup(r.content, 'html.parser')
        job_posting = []
        
        listings = soup.select(".job-post")
        for index, li  in enumerate(listings):
            title = getJobTitle(li)
            field = getJobField(li)
            raw_url = getRawUrl(li)
            job_type = getJobType(li)
            exp = getJobExperience(li)
            location = getJobLoc(li)
            
            job_posting.append(
                { index: 
                    {
                    "title": title, 
                    "field" : field,
                    "type": job_type, 
                    "experience": exp,
                    "loc": location, 
                    "r_url": raw_url
                    }
                }
            )
            
        return job_posting

def getJobTitle(listing) -> str:
    """Gets the job title from the listing

    Args:
        listing (bs4.element.tag): A complete html job listing

    Returns:
        str: The job title
    """
    
    title = listing.find(   
                href=re.compile("find-your-job/all/all/")
                ).text
    return title        
   

def getRawUrl(listing) -> str:
    """Retrieves the url from the listing

    Args:
        listing (bs4.element.tag): A complete html job listing

    Returns:
        str: Returns the type of job (full/part-time or intern)
    """
    url = listing.find(
            href=re.compile("find-your-job/all/all/")
            ).get('href')
    return url
        
def getJobType(listing) -> str:
    """Gets the type of job (full-time, part-time, or intern)

    Args:
        listing (bs4.element.tag): A complete html job listing

    Returns:
        str: Returns the type of job (full/part-time or intern)
    """
    
    j_type = listing.small.text.split('|')[1]
    return j_type
    

def getJobLoc(listing) -> str:
    """Gets the job location from the string

    Args:
        listing (bs4.element.tag): A complete html job listing

    Returns:
        str: Returns the location where the job is to
        be performed
    """
    
    loc = listing.find_all("small")[1].text.split("|")[1]
    return loc

def getJobExperience(listing) -> str:
    """Gets the level of experience preferred by the employer
    for this job

    Args:
        listing (bs4.element.tag): A complete html job listing

    Returns:
        str: Experience preferred by the employer (entry, mid, senior)
    """
    
    exp = listing.small.text.split('|')[0]
    return exp

def getJobField(listing) -> str:
    """Gets the field of the job

    Args:
        listing (bs4.element.tag): A complete html job listing

    Returns:
        str: The field associated with the job
    """
    
    field = listing.find_all("small")[1].text.split("|")[0]
    return field

getLLNLJob(["postdoc", "full-time"])
