from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

CONNECTION = "postgresql://evensch:swordfish@localhost/evensch"

orm_base = declarative_base()

class person(orm_base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True)
    legal_name = Column(String)
    guardian_id = Column(Integer, ForeignKey("persons.id"))
    contact_info = Column(String)

class year(orm_base):
    __tablename__ = "years"

    id = Column(Integer, primary_key=True)
    year = Column(String)

class day(orm_base):
    __tablename__ = "days"

    id = Column(Integer, primary_key=True)
    day = Column(String)

class validity(orm_base):
    __tablename__ = "validities"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    year_id = Column(String, ForeignKey("years.id"))

engine = create_engine(CONNECTION, echo=True)
mksession = sessionmaker(bind=engine)
session = mksession()

if __name__ == "__main__":
    import sys
    if "--drop" in sys.argv:
        orm_base.metadata.drop_all(engine)
    if "--create" in sys.argv:
        orm_base.metadata.create_all(engine)
