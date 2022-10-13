from sqlalchemy import Column, String, ForeignKey, Integer, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Table
from sqlalchemy.sql.sqltypes import Date




Base = declarative_base()


class Author(Base):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    birthday = Column(Date)
    bio = Column(String(150))
    quote = relationship("Quote")


assotiation_table = Table(
    "assotiation",
    Base.metadata,
    Column("keyword_id", ForeignKey("keyword.id")),
    Column("quote_id", ForeignKey("quote.id")),
)


class Keyword(Base):
    __tablename__ = "keyword"
    id = Column(Integer, primary_key=True)
    word = Column(String(40), nullable=False, unique=True)
    quotes = relationship(
        "Quote", secondary=assotiation_table, back_populates="keywords"
    )


class Quote(Base):
    __tablename__ = "quote"
    id = Column(Integer, primary_key=True)
    quote = Column(String, nullable=False, unique=True)
    author_id = Column(Integer, ForeignKey("author.id"))
    keywords = relationship(
        "Keyword", secondary=assotiation_table, back_populates="quotes"
    )
    