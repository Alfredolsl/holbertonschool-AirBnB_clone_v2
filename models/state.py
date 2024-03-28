#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from models.city import City
from models import storage


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade="all, delete, delete-orphan", backref="state")

    @property
    def cities(self):
        """Returns City instances where state_id equals to the
        current State.id"""
        storageObjects = storage.all()
        cityObjects = [obj for obj in storageObjects.values() if key.split()[0] == "City"]
        citySameID = [key for key in cityObjects if key.state_id == self.id]
        return citySameID
