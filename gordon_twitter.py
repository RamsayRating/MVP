#!/usr/bin/env python3
import twitter
import sqlite3
from sqlite3 import Error
from mongoengine import *
import os.path

import numpy as np
import math
from unidecode import unidecode
from watson_developer_cloud import ToneAnalyzerV3

import database as db

def list_field_to_dict(list_field):
    """
    Converts a list of mongodb Objects to a dictionary object

    list_field          list of embedded documents or other object types
    """

    return_data = []

    for item in list_field:
        # if list is of embedded documents, convert each document to a dictionary
        if isinstance(item, EmbeddedDocument):
            return_data.append(mongo_to_dict(item))
        # convert the data type
        else:
            return_data.append(mongo_to_python_type(item,item))

    return return_data

def mongo_to_python_type(field, data):
    """
    Converts certain fields to appropriate data types

    field       A field in a mongoDB object

    data        corresponding data to the field
    """
    if isinstance(field, ObjectIdField):
        return str(data)
    elif isinstance(field, DecimalField):
        return data
    elif isinstance(field, BooleanField):
        return data
    else:
        return str(data)

def mongo_to_dict(obj):
    """Get dictionary from mongoengine object
    id is represented as a string

    obj         A mongodb object that will be converted to a dictionary
    """
    return_data = []
    if obj is None:
        return None

    # converts the mongoDB id for documents to a string from an ObjectID object
    if isinstance(obj, Document):
        return_data.append(("id",str(obj.id)))

    for field_name in obj._fields:

        if field_name in obj:  # check if field is populated
            if field_name in ("id",):
                continue

            data = obj[field_name]
        
            if isinstance(obj._fields[field_name], ListField):
                return_data.append((field_name, list_field_to_dict(data)))
            elif isinstance(obj._fields[field_name], EmbeddedDocumentField):
                return_data.append((field_name, mongo_to_dict(data)))
            elif isinstance(obj._fields[field_name], DictField):
                return_data.append((field_name, data))
            else:
                return_data.append((field_name, mongo_to_python_type(obj._fields[field_name], data)))
            
    return dict(return_data)


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """

    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def sentiment_analysis(name, dictionary):
	"""
	This function takes a file and creates a dictionary of each line's sentiment analysis.
	>>> sentiment_analysis('EmmanuelMacron', {})
	{'EmmanuelMacron': [0.1466666666666667, 0.0, -0.1, 0.0, 0.42000000000000004, 0.0, 0.115, 0.0, 0.1325, 0.0, 0.03333333333333333, 0.0, 0.27, -0.12, 0.0, 0.22, 0.27, 0.1, 0.15, 0.075, 0.0, 0.0, 0.0, 0.17, 0.0, 0.07666666666666666, 0.2, 0.0, 0.0, 0.2, 0.2525, -0.35, 0.0, 0.0, 0.1, 0.0, 0.15, 0.0, 0.0, 0.56, 0.0, 0.25, 0.22, 0.0, 0.0, 0.45, 0.0, 0.0, 0.023333333333333334, 0.025000000000000022, 0.0, 0.0, -0.125, 0.0, 0.0, 0.0, 0.15, 0.13666666666666666, 0.1, 0.11, 0.0, 0.0, -0.4, 0.0, 0.0, 0.2, 0.625, 0.0, 0.0, 0.0, 0.09999999999999999, 0.0, 0.05, 0.25, 0.0, 0.0, 0.0, 0.22, 0.0, 0.22, 0.22, 0.53, -0.15, 0.0, 0.0, 0.4, 0.0, 0.0, 0.009999999999999995, 0.0, 0.0, -0.016666666666666663, 0.1, 0.0, 0.15, 0.0, 0.1, 0.0, -0.25, 0.0, -0.25166666666666665, 0.22, 0.17, 0.0, 0.0, -0.7, 0.0, 0.22, 0.22, 0.0, 0.2, 0.0, 0.0, 0.0, 0.13, 0.17, 0.0, 0.1275, 0.0, 0.0, 0.1, 0.15, -0.16249999999999998, 0.1, 0.8, 0.14, 0.0, 0.0, -0.1, 0.0, 0.0, 0.0, 0.30833333333333335, 0.0, 0.185, 0.0, 0.0, 0.0, -0.09000000000000001, 0.0, 0.08, -0.75, 0.22, 0.0, -0.3, 0.21000000000000002, 0.010000000000000009, -0.03125, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.17500000000000002, 0.3499999999999999, 0.09833333333333334, 0.135, 0.0, 0.0, 0.08, 0.2, 0.0, -0.2, 0.0, 0.2233333333333333, 0.0, 0.29, 0.0, 0.0, 0.0, 0.0, 0.6625000000000001, 0.29, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.32, 0.4, -0.24, 0.0, -0.125, 0.15, 0.0, 0.7, 0.0, 0.22, 0.0, 0.0, 0.5, 0.0, 0.2, -0.21875, 0.25, 0.26, 0.185, 0.08333333333333333, 0.23]}
	"""
	tone_analyzer = ToneAnalyzerV3(
		    username='2ed2f0c6-1722-472d-9126-224897b991af',
		    password='UcuSde1YmeK6',
		    version='2016-05-19')
	l = open(name + '.txt')
	lines = l.readlines()
	feel_dict = {'Anger':1.0,'Fear':2.0, 'Sadness':3.0, 'Disgust':4.0,'Joy':5.0, 'Excitement':6.0}
	dictionary[name] = []
	for i in lines:
		#print('-----------------')
		#print(i)
		max_score = 0.0
		max_feel = ''
		tone = tone_analyzer.tone(i, 'emotion')
		for feel in tone['document_tone']['tone_categories']:
			for feeling in feel['tones']:
				if feeling['score'] > max_score:
					max_score = feeling['score']
					max_feel = feeling['tone_name']
		#print(max_score, max_feel)
		#blob1 = TextBlob(i, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
		if max_feel != '':
			tweet_tbu = db.Tweet.objects(rating=feel_dict[max_feel]).first()
			dict_tbu = {}
			if tweet_tbu:
				dict_tbu = mongo_to_dict(tweet_tbu)
				print('exists')
				print(dict_tbu)
				if max_feel != '':
					new_dict = {}
					new_dict['tweet'] = dict_tbu['tweet']
					new_dict['tweet'].append(i[0:-2])
					tweet_tbu.update(**new_dict)
					tweet_tbu.reload()
			else:
				print('not exists - with max')
				new_dict = {}
				new_dict['tweet'] = [i[0:-1]]
				if max_feel != '':
					new_dict['rating'] = feel_dict[max_feel]
				else:
					new_dict['rating'] = 0.0
				print(new_dict)
				new_tweet = db.Tweet(**new_dict)
				new_tweet.save()
		else:
			print('not exists - without')
			new_dict = {}
			new_dict['tweet'] = [i[0:-1]]
			if max_feel != '':
				new_dict['rating'] = feel_dict[max_feel]
			else:
				new_dict['rating'] = 0.0
			print(new_dict)
			new_tweet = db.Tweet(**new_dict)
			new_tweet.save()
	result = db.Tweet.objects()
	return(result)


def retrieve_tweets():
	result = db.Tweet.objects()
	converted_dict = {}
	for tweet_section in result:
		converted_dict = mongo_to_dict(tweet_section)
		print(converted_dict)
	return(converted_dict)


def retrieve_text(name, number):
	consumer_k = open('consumer_key.txt').read().strip()
	consumer_s = open('consumer_secret.txt').read().strip()
	access_key = open('access_token_key.txt').read().strip()
	access_secret = open('access_token_secret.txt').read().strip()
	api = twitter.Api(consumer_key=	consumer_k,
                  consumer_secret= consumer_s,
                  access_token_key= access_key,
                  access_token_secret= access_secret)

	l = open(name + '.txt', 'w')
	status = api.GetUserTimeline(screen_name='@' + name, count = number)

	for i in status:

		i = unidecode(i.text)
		if "MasterChef" not in i and "HellsKitchen" not in i \
			and "MASTERCHEF" not in i and "#" not in i and "@" not in i:
			j = i.split(" ")
			j = j[0:-1]
			i = ' '.join(word for word in j)
			print(i)
			l.write(i)
			l.write('\n')
		
	l.close()

#retrieve_text('GordonRamsay', 203)
sentiments = {}
sentiment_analysis('GordonRamsay', sentiments)
results = retrieve_tweets()
print(results)

