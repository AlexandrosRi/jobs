from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#read local value for sqlite
engine = create_engine('sqlite',
                       convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata. Otherwise
    # you will have to import them first before calling init_db()
    import jobs.models
    Base.metadata.create_all(bind=engine)


def drop_db():
    Base.metadata.drop_all(bind=engine)

def populate_db():
	# adds careernet.gr and kariera.gr
    from jobs.models import Source

    kariera = Source(name="kariera",
                    baseUrl="http://www.kariera.gr/",
                    queryVar="έρευνα?q",
                    locationVar="loc",
                    pagerVar="pg",
                    hrefTag=".job-list h3 a",
                    titleTag=".job-list h3 a",
                    pagTag=".pagination li",
                    pagLength=2)
    careernet = Source(name="careernet",
                    baseUrl="http://www.careernet.gr/",
                    queryVar="aggelies?keywords",
                    locationVar="",
                    pagerVar="page",
                    hrefTag=".aggelia-list-group .col-xs-12 header a",
                    titleTag=".aggelia-list-group .col-xs-12 header a h2",
                    pagTag=".pagination li",
                    pagLength=1)

    db_session.add(kariera)
    db_session.add(careernet)

    db_session.commit()
