#!/usr/bin/python3
"""Representation of a database storage for HBNB project."""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """Represents a database."""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiates a DBStorage object.
        Creates engine and connects to db."""
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        db = getenv("HBNB_MYSQL_DB")
        host = getenv("HBNB_MYSQL_HOST")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}"
                                      .format(user, password, host, db),
                                      pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary"""
        dictionary = {}
        if cls:
            query = self.__session.query(cls)
            for elem in query:
                key = "{}.{}".format(type(elem).__name__, elem.id)
                dictionary[key] = elem
        else:
            class_list = [State, City, User, Place, Review, Amenity]
            for cls in class_list:
                query = self.__session.query(cls)
                for elem in query:
                    key = "{}.{}".format(type(elem).__name__, elem.id)
                    dic[key] = elem

        return dictionary

    def new(self, obj):
        """adds object to current db session"""
        self.__session.add(obj)

    def save(self):
        """commits changes to current db session"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes object from current db session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Creates the current session from db engine."""
        # Create table
        Base.metadata.create_all(self.__engine)
        # Establish calls to the db
        current_session = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        # scoped_session produces a managed registry of Session objects
        # Threads manage user requests and db operations
        Session = scoped_session(current_session)
        self.__session = Session()
