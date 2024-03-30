#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Table, Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

place_amenity = Table("place_amenity", Base.metadata,
                      Column("place_id", String(60), ForeignKey("places.id"),
                             primary_key=True, nullable=False),
                      Column("amenity_id", String(60), ForeignKey("amenities.id"),
                             primary_key=True, nullable=False)
                     )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    reviews = relationship("Review", backref="place", cascade="all, delete")
    amenities = relationship("Amenity", secondary=place_amenity,
                             viewonly=False)

    
    @property
    def reviews(self):
        """Getter attribute for reviews.
        Returns list of Review instances if
        place_id is equal to current Place.id"""
        from models import storage
        extracted_reviews = storage.all("Review").values()
        filtered_reviews = [review for review in extracted_reviews
                            if review.place_id == self.id]
        return filtered_reviews

    @property
    def amenities(self):
        """Getter attribute for amenities.
        Returns list of Amenity instances if
        amenity_ids linked to the Place."""
        from models import storage
        extracted_amenities = storage.all("Amenity").values()
        filtered_amenities = [amenity for amenity in extracted_amenities
                              if amenity.amenity_ids == self.id]
        return filtered_amenities

    @amenities.setter
    def amenities(self, obj):
        """amenities setter attribute.
        Handles append method for adding
        and Amenity.id to the attribute
        amenity_ids"""
        if isinstance(obj, "Amenity"):
            self.amenity_id.append(obj.id)
