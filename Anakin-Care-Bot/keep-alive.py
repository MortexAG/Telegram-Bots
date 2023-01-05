import flask
from flask import Flask, render_template
import random
import threading
from threading import Thread
import pymongo 
from pymongo import MongoClient
import os

mongo_connect = os.environ['mongo_connect']
cluster = MongoClient(mongo_connect)
db = cluster["anakin_care"]
food = db['food_time']

app = Flask(__name__,template_folder = "templatefiles", static_folder= "staticfiles")

@app.route('/')
def main():
  feeding = food.find_one({"_id":0})
  feeder = feeding['feeder']
  last_time = feeding['last_time']
  next_time = feeding['next_time']
  return render_template("index.html", feeders = feeder , last = last_time, next = next_time )

def run():
  app.run(
    host="0.0.0.0",
    port=random.randint(2000,9000)
  )

def keep_alive():
  t = Thread(target=run)
  t.start()

keep_alive()
