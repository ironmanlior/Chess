#!/usr/bin/python

from __future__ import annotations
import mongoengine as db
from datetime import date
import re

class User(db.Document):
    username = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
    full_name = db.StringField(required=True)
    email = db.EmailField(required=True)
    birthday = db.DateField(required=True)
    admin = db.BooleanField(default=False)
    logged_in = db.BooleanField(default=True)
    friends = db.ListField(db.ReferenceField("self"))
    rating = db.IntField(min_value=0, default=1200)
    rating_history = db.ListField(db.IntField(min_value=0, default=1200))
    
    def __init__(self, username: str, password: str, full_name: str, email: str, birthday: date, rating=1200, admin=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = username
        self.password = password
        self.full_name = full_name
        self.email = email
        self.birthday = birthday
        self.logged_in = True
        self.admin = admin
        self.friends = []
        self.rating = rating
        self.rating_history = [rating]
    
    @db.queryset_manager
    def objects(cls, query: db.QuerySet) -> db.QuerySet:
        return query
    
    @classmethod
    def find(cls, username: str, password: str) -> User:
        try:
            query: db.QuerySet = cls.objects(username=username, password=password)
            if not query.first(): raise
            return query.first()
        except Exception as e:
            raise db.ValidationError("username or password are Invalid")
    
    def Login(self):
        if self.logged_in:
            raise db.ValidationError("user already logged in")
        self.update(logged_in = True)
    
    def Logout(self):
        if not self.logged_in:
            raise db.ValidationError("user not logged in")
        self.update(logged_in = False)    
    
    def add_friend(self, friend: User):
        self.friends.append(friend)
        self.update(friends = self.friends)
    
    def end_game(self, rating: int, k: int, score: float):
        e_score: float = 1 / (1 + 10 ** ((rating - self.rating) / 400))
        self.rating += k * (score - e_score)
        self.rating_history.append(self.rating)
        self.update(rating=self.rating, rating_history=self.rating_history)
        
    
    def __clean_date(self) -> bool:
        today = date.today()
        con = any([
            self.birthday.year < today.year,
            self.birthday.year == today.year and self.birthday.month < today.month,
            self.birthday.year == today.year and self.birthday.month == today.month and self.birthday.day < today.day
        ])
        if self.birthday.day <= 0 or self.birthday.month <= 0 or self.birthday.year <= 0:
            return False
        elif self.birthday.month in [1, 3, 5, 7, 8, 10, 12] and self.birthday.day <= 31:
            return con
        elif self.birthday.month in [4, 6, 9, 11] and self.birthday.day <= 30:
            return con
        elif self.birthday.month == 2 and self.birthday.day <= 28:
            return con
        elif self.birthday.year % 4 == 0 and self.birthday.month == 2 and self.birthday.day == 29:
            return con
        return False
    
    def clean(self):
        if self.username == "":
            raise db.ValidationError(f"Invalid username: {self.username}")
        if " " not in self.full_name:
            raise db.ValidationError(f"Invalid full name: {self.full_name}")
        valid = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
        if re.search(valid, self.email) == None:
            raise db.ValidationError(f"Invalid email: {self.email}")
        if not self.__clean_date():
            raise db.ValidationError(f"Invalid date: {self.birthday.day}.{self.birthday.month}.{self.birthday.year}")
    
