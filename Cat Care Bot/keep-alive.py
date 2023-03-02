import flask
from flask import Flask, render_template
import random
import threading
from threading import Thread
import pymongo 
from pymongo import MongoClient
import os

mongo_connect = os.environ['mongo_connect']
owner_1 = str(os.environ['owner_1'])
owner_2 = str(os.environ['owner_2'])
owners_list = [owner_1, owner_2]
cluster = MongoClient(mongo_connect)
db = cluster["anakin_care"]
food = db['food_time']
points = db['points']

app = Flask(__name__,template_folder = "templatefiles", static_folder= "staticfiles")

@app.route('/')
def main():
  feeding = food.find_one({"_id":0})
  feeder = feeding['feeder']
  last_time = feeding['last_time']
  next_time = feeding['next_time']
  points_list= []
  for user in owners_list:
    user = int(user)
    the_user = points.find_one({"_id":user})
    user_points = the_user['points']
    username = the_user['username']
    result = f"{username}: "+" "+user_points+"😸"
    points_list.append(result)  
  leaderboard = "\n".join(points_list)
  return render_template("index.html", feeders = feeder , last = last_time, next = next_time, leaderboard = points_list)

def run():
  app.run(
    host="0.0.0.0",
    port=random.randint(2000,9000)
  )

def keep_alive():
  t = Thread(target=run)
  t.start()

keep_alive()
