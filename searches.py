import requests
import bs4
from flask_sqlalchemy import SQLAlchemy
from jobs import models


def searchJobs(jobSite, keyword, location):
    baseUrl = jobSite.baseUrl + jobSite.queryVar + '='
    pg = 1
    lastPageNum = 1
    locvar = "" if jobSite.locationVar == None else jobSite.locationVar
    url = baseUrl + keyword + '&' + locvar + '=' + location
    url = url + '&' + jobSite.pagerVar + '=' + str(pg)
    print(url)
    res = requests.get(url)
    res.raise_for_status()
    jobsPage = bs4.BeautifulSoup(res.text, 'html.parser')
    jobsPaginator = jobsPage.select(jobSite.pagTag)
    if jobsPaginator:
        lastPageNum = int(jobsPaginator[len(jobsPaginator) - jobSite.pagLength].getText())


    jobs = []

    while pg <= lastPageNum:
        res = requests.get(url)
        res.raise_for_status()
        jobsPage = bs4.BeautifulSoup(res.text, 'html.parser')
        jobsHref = jobsPage.select(jobSite.hrefTag)
        if (jobSite.hrefTag == jobSite.titleTag):
            jobsTitle = jobsHref
        else:
            jobsTitle = jobsPage.select(jobSite.titleTag)


        for i in range(len(jobsHref)):
            jobs.append([
                        jobsTitle[i].getText(),
                        jobSite.baseUrl + str(jobsHref[i].get('href'))])
        pg = pg + 1
        url = baseUrl + keyword + '&' + locvar + '=' + location
        url = url + '&' + jobSite.pagerVar + '=' + str(pg)
        print("url " + str(pg) + " : " + url)

    return jobs


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

        for i in range(len(jobsElem)):
            jobs.append([
                        jobsElem[i].getText(),
                        str(jobsElem[i].get('href'))])
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
