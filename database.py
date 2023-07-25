import csv
from sqlalchemy import create_engine, Table, Column, Integer, String, Date, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"

Base = declarative_base()


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    rubrics = Column(ARRAY(String), index=True)
    text = Column(String)
    created_date = Column(Date, index=True)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)
    load_csv_to_db()


def load_csv_to_db():
    session = SessionLocal()
    if not session.query(Document).first():
        with open("posts.csv", "r") as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                document = Document(
                    id=int(row["id"]),
                    rubrics=row["rubrics"].split(","),
                    text=row["text"],
                    created_date=row["created_date"],
                )
                session.add(document)
            session.commit()
            session.close()
