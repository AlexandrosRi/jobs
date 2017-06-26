import requests
import bs4
from flask_sqlalchemy import SQLAlchemy
from jobs import models
from functools import lru_cache
import itertools
import json
from jellyfish import levenshtein_distance, damerau_levenshtein_distance, hamming_distance, jaro_distance, jaro_winkler


def searchJobs(jobSite, keyword, location, area=""):

    """
    if jobSite.baseUrl:
        extrBaseUrl = jobSite.baseUrl
    else:
        extrBaseUrl = ""
    """
    baseUrl = "" if not jobSite.baseUrl else jobSite.baseUrl
    #baseUrl = extrBaseUrl + jobSite.queryVar + '='
    pg = 1
    lastPageNum = 1
    # url = baseUrl + keyword + '&' + locvar + '=' + location

    queryUrl = jobSite.formatedURL.format(keyword=keyword,
                                          location=location, area=area)

    url = queryUrl  # + '&' + jobSite.pagerVar + '=' + str(pg)

    # res = requests.get(url)
   # res.raise_for_status()

    try:
        res = requests.get(url)
        res.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        return []

    jobsPage = bs4.BeautifulSoup(res.text, 'html.parser')

    jobsPaginator = "" if not jobSite.pagTag else jobsPage.select(jobSite.pagTag)
    # print(jobsPaginator[len(jobsPaginator) - jobSite.pagLength].getText())

    if jobsPaginator:
        lastPageNum = int(jobsPaginator[len(jobsPaginator) - jobSite.pagLength].getText())

    jobs = []

    while pg <= lastPageNum:
        res = requests.get(url)
        print(url + " with status: " + str(res.status_code))

        #res.raise_for_status()
        jobsPage = bs4.BeautifulSoup(res.text, 'html.parser')

        # ad link
        jobsHref = jobsPage.select(jobSite.hrefTag)

        # ad title
        if (jobSite.hrefTag == jobSite.titleTag):
            jobsTitle = jobsHref
        else:
            jobsTitle = jobsPage.select(jobSite.titleTag)

        # ad company
        """jobsComp = [""]
        if jobSite.compTag:
            jobsComp = jobsPage.select(jobSite.compTag)
        print("comp: " + str(len(jobsComp)))"""

        # ad area 
        jobsRow = jobsPage.select(jobSite.jobTag)
        # print(jobSite.name + " compTag " + str(bool(jobSite.compTag)))  

        for i in range(len(jobsHref)):
            if (jobSite.compTag and len(jobsRow[i].select(jobSite.compTag)) > 0):
                jobs.append([
                            jobsTitle[i].getText(),
                            baseUrl + str(jobsHref[i].get('href')),
                            jobsRow[i].select(jobSite.compTag)[0].getText(),
                            jobsRow[i].select(jobSite.areaTag)[0].getText().replace("Περιοχή", "").strip() if jobSite.areaTag else " ",
                            jobSite.name, 0
                            ])
            else:
                jobs.append([
                            jobsTitle[i].getText(),
                            baseUrl + str(jobsHref[i].get('href')),
                            " ",
                            jobsRow[i].select(jobSite.areaTag)[0].getText().replace("Περιοχή", "").strip(),
                            jobSite.name, 0
                            ])
            
        pg = pg + 1
        #url = baseUrl + keyword + '&' + locvar + '=' + location
        url = queryUrl + '&' + jobSite.pagerVar + '=' + str(pg)

    return jobs


@lru_cache(maxsize=16)
def saveJobs(kw, loc, area):

    sources = models.Source.query.all()

    areas = getListedAreas()

    jobs = []
    for src in sources:
        print("Fetching from: ")
        print(src.name)

        srcAreas = None

        if area:
            srcAreas = areas[src.name][area]

        if isinstance(srcAreas, list):
            for srcArea in srcAreas:
                tmp = searchJobs(src, kw.replace(' ', '+'), loc.replace(' ', '+'), srcArea.replace(' ', '+'))
                jobs = list(itertools.chain(jobs, tmp))
        elif isinstance(srcAreas, str):
            tmp = searchJobs(src, kw.replace(' ', '+'), loc.replace(' ', '+'), srcAreas.replace(' ', '+'))
            jobs = list(itertools.chain(jobs, tmp))
        else:
            tmp = searchJobs(src, kw.replace(' ', '+'), loc.replace(' ', '+'))
            jobs = list(itertools.chain(jobs, tmp))

    return jobs


@lru_cache(maxsize=16)
def getListedAreas():
    with open('jobs\\static\\areas-matching.json', encoding="utf-8") as areas:
        areas = json.load(areas, encoding="utf-8")

    return areas


# @lru_cache(maxsize=16)
def orderByRel(jobs, kw, algo):
    """Order based on algo type"""
    for i in range(len(jobs)):
        if algo == 1:
            jobs[i][5] = levenshtein_distance(jobs[i][0].strip(), kw)


        elif algo == 2:
            jobs[i][5] = damerau_levenshtein_distance(jobs[i][0].strip(), kw)

        elif algo == 3:
            jobs[i][5] = hamming_distance(jobs[i][0].strip(), kw)

        elif algo == 4:
            jobs[i][5] = 1 - jaro_distance(jobs[i][0].strip(), kw)

        elif algo == 5:
            jobs[i][5] = 1 - jaro_winkler(jobs[i][0].strip(), kw)

    # jobs.sort(jobs, key=lambda job: job[5])
    jobs_sorted = sorted(jobs, key=lambda dist: dist[5])

    return jobs_sorted




"""
    
def searchKariera(keyword, location):
    kariera = models.Source.query.filter_by(name='kariera').first()
    baseUrl = kariera.baseUrl + kariera.queryVar + '='
    pg = 1
    url = baseUrl + keyword + '&' + kariera.locationVar + '=' + location
    url = url + '&' + kariera.pagerVar + '=' + str(pg)
    res = requests.get(url)
    res.raise_for_status()
    jobsPage = bs4.BeautifulSoup(res.text, 'html.parser')
    jobsElem = jobsPage.select('.job-list h3 a')
    jobsNum2 = jobsPage.select('.pagination li')
#    lastPageStr = jobsNum2[len(jobsNum2) - 2].getText()
    lastPageNum = int(jobsNum2[len(jobsNum2) - 2].getText())
    jobs = []

    while not pg > lastPageNum:
        res = requests.get(url)
        res.raise_for_status()
        jobsPage = bs4.BeautifulSoup(res.text, 'html.parser')
        jobsElem = jobsPage.select('.job-list h3 a')
       # jobsCompany = jobsPage.select('.job-list .row p a.show-for-large-up')
        TODO
        select area
        get text
        jobsCompany = jobsPage.select('.job-list .row
        for j in jobsElem:
...     tL.append(j.select('ul li:nth-of-type(1):nth-of-type(2)'))
        remove words

        for i in range(len(jobsElem)):
            jobs.append([
                        jobsElem[i].getText(),
                        str(jobsElem[i].get('href')),])
        pg = pg + 1
        url = baseUrl + keyword + '&loc=' + location + '&pg=' + str(pg)

    return jobs


def searchCareernet(keyword):
    baseUrl = 'http://www.careernet.gr/aggelies?keywords='
    pg = 1
    lastPageNum = 1
    url = baseUrl + keyword + '&page=' + str(pg)
    res = requests.get(url)
    res.raise_for_status()
    jobsPage = bs4.BeautifulSoup(res.text, 'html.parser')
    jobsNum2 = jobsPage.select('.pagination li')
#    lastPageStr = jobsNum2[len(jobsNum2) - 2].getText()
    if jobsNum2:
        lastPageNum = int(jobsNum2[len(jobsNum2) - 1].getText())
    jobs = []

    while pg <= lastPageNum:
        res = requests.get(url)
        res.raise_for_status()
        jobsPage = bs4.BeautifulSoup(res.text, 'html.parser')
        jobsElem = jobsPage.select('.aggelia-list-group .col-xs-12 header a h2')

        baseAggelia = 'http://www.careernet.gr'
        for i in range(len(jobsElem)):
            print(jobsElem[i].contents)
            jobs.append([
                        jobsElem[i].getText(),
                        baseAggelia + str(jobsElem[i].get('href'))])
        pg = pg + 1
        url = baseUrl + keyword + '&page=' + str(pg)

    return jobs
"""