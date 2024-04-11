#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Table, Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv

place_amenity = Table("place_amenity", Base.metadata,
                      Column("place_id",
                             String(60),
                             ForeignKey("places.id"),
                             primary_key=True,
                             nullable=False),
                      Column("amenity_id",
                             String(60),
                             ForeignKey("amenities.id"),
                             primary_key=True,
                             nullable=False)
                      )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=False)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    amenity_ids = []
    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship("Review",
                               cascade="delete",
                               backref="place")
        amenities = relationship("Amenity",
                                 secondary="place_amenity",
                                 backref="places",
                                 viewonly=False)
    else:
        @property
        def reviews(self):
            """Getter attribute for reviews.
            Returns list of Review instances if
            place_id is equal to current Place.id"""
            from models import storage
            from models.review import Review
            extracted_reviews = storage.all(Review).values()
            filtered_reviews = []

            for review in extracted_reviews:
                if review.state_id == self.id:
                    filtered_reviews.append(review)

            return filtered_reviews

        @property
        def amenities(self):
            """Getter attribute for amenities.
            Returns list of Amenity instances if
            amenity_ids linked to the Place."""
            from models import storage
            from models.amenity import Amenity
            extracted_amenities = storage.all(Amenity).values()
            amenity_list = []

            for amenity in extracted_amenities:
                if amenity.id in self.amenity_ids:
                    amenity_list.append(amenity)
            
            return amenity_list

        @amenities.setter
        def amenities(self, obj):
            """amenities setter attribute.
            Handles append method for adding
            and Amenity.id to the attribute
            amenity_id"""
            from models.amenity import Amenity
            if type(obj) is Amenity:
                self.amenity_ids.append(obj.id)
