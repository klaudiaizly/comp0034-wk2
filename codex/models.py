# Adapted from https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/quickstart/#define-models
from typing import List
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from codex import db


# This uses the latest syntax for SQLAlchemy, older tutorials will show different syntax
# SQLAlchemy provide an __init__ method for each model, so you do not need to declare this in your code
class Cases(db.Model):
    __tablename__ = "cases"
    case_id: Mapped[str] = mapped_column(db.Text, primary_key=True)
    case_type: Mapped[str] = mapped_column(db.Text, nullable=False)
    status: Mapped[str] = mapped_column(db.Text, nullable=True)
    case_active_days_at_closure: Mapped[int] = mapped_column(db.Integer, nullable=True)
    closed_on_time: Mapped[str] = mapped_column(db.Text, nullable=True)
    request_recieved_date: Mapped[str] = mapped_column(db.Text, nullable=True)
    request_closed_date: Mapped[str] = mapped_column(db.Text, nullable=True)
    # one-to-many relationship with Event, the relationship in Event is called 'region'
    # https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#one-to-many
    events: Mapped[List["Recieved_Date"]] = relationship(back_populates="cases")


class Recieved_Date(db.Model):
    __tablename__ = "recieved_date"
    date_id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    request_recieved_date: Mapped[int] = mapped_column(ForeignKey("cases.request_recieved_date"))
    # add relationship to the parent table, Region, which has a relationship called 'events'
    cases: Mapped["Cases"] = relationship("Cases", back_populates="recieved_date")
    request_recieved_month: Mapped[str] = mapped_column(db.Text, nullable=True)
    request_recieved_year: Mapped[str] = mapped_column(db.Text, nullable=True)
    

class Closed_Date(db.Model):
    __tablename__ = "closed_date"
    date_id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    request_closed_date: Mapped[int] = mapped_column(ForeignKey("cases.request_recieved_date"))
    # add relationship to the parent table, Region, which has a relationship called 'events'
    cases: Mapped["Cases"] = relationship("Cases", back_populates="closed_date")
    request_closed_month: Mapped[str] = mapped_column(db.Text, nullable=True)
    request_closed_year: Mapped[str] = mapped_column(db.Text, nullable=True)


class Recieved_Quarter(db.Model):
    __tablename__ = "recieved_quarter"
    month_id:Mapped[int] = mapped_column(db.Integer, primary_key=True)
    request_recieved_month: Mapped[int] = mapped_column(ForeignKey("recieved_date.request_recieved_month"))
    request_recieved_quarter: Mapped[str] = mapped_column(db.Text, nullable=True)
    recieved_date: Mapped["Recieved_Date"] = relationship("recieved_date", back_populates="recieved_quarter")
    
class Closed_Quarter(db.Model):
    __tablename__ = "closed_quarter"
    month_id:Mapped[int] = mapped_column(db.Integer, primary_key=True)
    request_closed_month: Mapped[int] = mapped_column(db.Integer, nullable=True)
    request_closed_quarter: Mapped[str] = mapped_column(db.Text, nullable=True)
    closed_date: Mapped["Closed_Date"] = relationship("closed_date", back_populates="closed_quarter")



    def __init__(self, email: str, password: str):
        """
        Create a new User object using hashing the plain text password.
        :type password_string: str
        :type email: str
        :returns None
        """
        self.email = email
        self.password = password

