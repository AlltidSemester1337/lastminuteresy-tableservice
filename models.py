from database import Base
from sqlalchemy import Column, Integer, String, DateTime

class Bookings(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True, index=True)
    restaurant = Column(String)
    time = Column(DateTime)