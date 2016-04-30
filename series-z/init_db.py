from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, configure_mappers
from models import *

print("Starting script.")


Base = declarative_base()

def init_db(db_name):
    engine = create_engine('sqlite:///%s.db' % (db_name), echo=True)
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))
    Base.query = db_session.query_property()
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    configure_mappers()
    Base.metadata.create_all(bind=engine)

    # Session = sessionmaker(bind=engine)
    # s = Session()
    print("Models created.")
    return db_session()


if __name__ == '__main__':
    init_db("series-z")