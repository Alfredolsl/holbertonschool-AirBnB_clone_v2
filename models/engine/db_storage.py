#!/usr/bin/python3
"""Database Storage for HBNB project."""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """Create tables"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiation of DBStorage"""
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@localhost/{}'
                                      .format(user, password, host, db), pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary"""
        queryDict = {}
        if cls:
            query = DBStorage.__session.query(cls)
            for elem in query:
                key = "{}.{}".format(type(elem).__name__, elem.id)
                queryDict[key] = elem
        else:
           allClasses = [State, City, User, Place, Review, Amenity]
           for cls in allClasses:
               query = DBStorage.__session.query(cls)
               for elem in query:
                   key = "{}.{}".format(type(elem).__name__, elem.id)
                   queryDict[key] = elem
        return queryDict

    def new(self, obj):
        """adds a new element to the table"""
        DBStorage.__session.add(obj)

    def save(self):
        """saves changes to the table"""
        DBStorage.__session.commit()

    def delete(self, obj=None):
        if obj:
            DBStorage.__session.delete(obj)

    def reload(self):
        """Creates the current session from the db engine."""
        # creates table
        Base.metadata.create_all(self.__engine)
        # establishes calls to the db
        currentSession = sessionmaker(bind=self.__engine, expire_on_commit=False) 
        # scoped_session produces a managed registry of Session objects (thread safety)
        # threads manage user requests and db operations.
        Session = scoped_session(currentSession)
        DBStorage.__session = Session()
