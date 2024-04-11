#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.city import City
from os import getenv


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship("City", cascade="all, delete, delete-orphan",
                              backref="state")

    else:
        @property
        def cities(self):
            """Getter attribute, returns a list"""
            from models import storage
            from models.city import City
            my_list = []
            extracted_cities = storage.all(City).values()
            for city in extracted_cities:
               if self.id == city.state_id:
                   my_list.append(city)
            return my_list

            #all_objects = models.storage.all()
            #filtered_cities = []

            #for key, val in all_objects.items():
            #    if "City" in key:
            #        filtered_cities.append(key[val])
            #return [city for city in filtered_cities if city.state_id == self.id]
