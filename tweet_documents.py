#!/usr/bin/env python3
"""Document models for mongoengine"""
from mongoengine import *
from bson import ObjectId

class Tweet(Document):
	tweet = ListField(StringField())
	rating = FloatField()