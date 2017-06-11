from flask import Flask, redirect, url_for
from flask import render_template, request, session

#import requests, bs4, math
import itertools

from jobs import app
from jobs import searches

@app.route('/', methods=['GET', 'POST'])
def search():
    """Initiates the search."""
    error = None

    if request.method == 'POST':
        if not request.form['keyword']:
            error = 'You have to enter a keyword'
        elif not request.form['location']:
            error = 'You have to enter a location'
        else:
            class Quer:
                def __init__(self, kw, loc):
                    self.kw = kw  # instance variable unique to each instance
                    self.loc = loc

            que = Quer(request.form['keyword'], request.form['location'])

            return redirect(url_for('apotelesmata', loc=que.loc, kw=que.kw))
    return render_template('search.html', error=error)


@app.route('/apotelesmata/<loc>/<kw>', methods=['GET', 'POST'])
def apotelesmata(loc, kw):
    """Displays the search results."""
    error = None
    jobs1 = searches.searchKariera(kw.replace(' ', '+'), loc.replace(' ', '+'))
    jobs2 = searches.searchCareernet(kw.replace(' ', '+'))
    jobs = itertools.chain(jobs1, jobs2)
    return render_template('results.html',
                           error=error, loc=loc, kw=kw, jobs=jobs)

# for i in range(len(jobsElem)):
# 	print(jobs[i][0])
