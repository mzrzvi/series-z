from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *

print("Starting script.")

engine = create_engine('sqlite:///seriesz.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
# Base = declarative_base()
# Base.query = db_session.query_property()

def init_db():
  # import all modules here that might define models so that
  # they will be registered properly on the metadata.  Otherwise
  # you will have to import them first before calling init_db()
  Base.metadata.create_all(bind=engine)
  print("Models created.")


if __name__ == '__main__':
  init_db()