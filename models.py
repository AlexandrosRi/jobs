from sqlalchemy import Column, Integer, String
from jobs.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True)
    email = Column(String(120), unique=True)

    """
    def __init__(self, username, email):
        self.username = username
        self.email = email
    """

    def __repr__(self):
        return '<User %r>' % self.username


class Source(Base):
    __tablename__ = 'sources'
    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    formatedURL = Column(String(120))
    baseUrl = Column(String(120))
    queryVar = Column(String(120))
    locationVar = Column(String(120))
    pagerVar = Column(String(120))
    hrefTag = Column(String(120))
    titleTag = Column(String(120))
    jobTag = Column(String(120))
    compTag = Column(String(120))
    areaTag = Column(String(120))
    pagTag = Column(String(120))
    pagLength = Column(Integer)
    """
    def __init__(self, name, baseUrl, pagerVar, locationVar, queryVar):
        self.name = name
        self.baseUrl = baseUrl
        self.pagerVar = pagerVar
        self.locationVar = locationVar
        self.queryVar = queryVar
    """

    def __repr__(self):
        return '<Source %r>' % self.name
