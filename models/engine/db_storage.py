#!/usr/bin/python3
"""Database Storage for HBNB project."""
from os import getenv
from sqlalchemy import create_engine
from models.base_model import Base

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
            query = self.__session.query(cls)
            for elem in query:
                key = "{}.{}".format(type(elem).__name__, elem.id)
                queryDict[key] = elem
        else:
            
