from flask import Flask, redirect, url_for
from flask import render_template, request, session
from flask_paginate import Pagination, get_page_args

#import requests, bs4, math
import itertools

from jobs import app
from jobs import searches
from jobs import models
from jobs.database import db_session


@app.route('/', methods=['GET', 'POST'])
def startSearch():
    """Initiates the search."""
    error = None

    if request.method == 'POST':
        if not request.form['keyword']:
            error = 'You have to enter a keyword'
        else:
            class Quer:
                def __init__(self, kw, loc, area):
                    self.kw = kw  # instance variable unique to each instance
                    self.loc = loc
                    self.area = area

            que = Quer(request.form['keyword'], request.form['location'],
                       request.form['listed-location'])
            return redirect(url_for('apotelesmata', loc=que.loc,
                                    kw=que.kw, area=que.area))
    return render_template('search.html', error=error)


@app.route('/apotelesmata/<kw>/', defaults={'page': 1, 'order': 0}, methods=['GET', 'POST'])
@app.route('/apotelesmata/<kw>', defaults={'page': 1, 'order': 0}, methods=['GET', 'POST'])
@app.route('/apotelesmata/<kw>/order/<int:order>/', defaults={'page': 1}, methods=['GET', 'POST'])
@app.route('/apotelesmata/<kw>/order/<int:order>', defaults={'page': 1}, methods=['GET', 'POST'])
@app.route('/apotelesmata/<kw>/page/<int:page>/', defaults={'order': 0}, methods=['GET', 'POST'])
@app.route('/apotelesmata/<kw>/page/<int:page>', defaults={'order': 0}, methods=['GET', 'POST'])
@app.route('/apotelesmata/<kw>/page/<int:page>/order/<int:order>/', methods=['GET', 'POST'])
@app.route('/apotelesmata/<kw>/page/<int:page>/order/<int:order>', methods=['GET', 'POST'])
def apotelesmata(kw, page, order):
    """Displays the search results."""
    error = None

    loc = request.args.get('loc')
    area = request.args.get('area')
    
    # sources = models.Source.query.all()
    jobs = searches.saveJobs(kw, loc, area)

    ttlCount = len(jobs)

    if order in range(1, 6):
        jobs = searches.orderByRel(jobs, kw, order)

    print("ttlCount: " + str(ttlCount))
    page, per_page, offset = get_page_args(per_page_parameter="20")

    pageJobs = jobs[offset:offset + per_page]

    pagination = Pagination(page=page, total=ttlCount, per_page=per_page,
                            record_name='jobs', css_framework='bootstrap3')

    return render_template('results.html',
                           error=error,
                           loc=loc, kw=kw, jobs=pageJobs,
                           page=page, per_page=per_page,
                           pagination=pagination, order=order, area=area
                           )


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
