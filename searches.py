import requests
import bs4
from flask_sqlalchemy import SQLAlchemy
from jobs import models


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
            jobs.append([jobsElem[i].getText(), str(jobsElem[i].get('href'))])
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
        jobsElem = jobsPage.select('.aggelia-list-group .col-xs-12 header a')

        baseAggelia = 'http://www.careernet.gr'
        for i in range(len(jobsElem)):
            print(jobsElem[i].contents)
            jobs.append([
                        jobsElem[i].h2.getText(),
                        baseAggelia + str(jobsElem[i].get('href'))])
        pg = pg + 1
        url = baseUrl + keyword + '&page=' + str(pg)

    return jobs
