#!/usr/bin/python

import mongoengine as db
import pymongo

client = pymongo.MongoClient()
chess_db = client["Chess"]
chess_db["User"]
chess_db["GameDB"]

db.connect("Chess", host="localhost", port=27017)

from . import user
from . import game_db
from .user import User
from .game_db import GameDB
