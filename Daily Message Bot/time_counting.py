import datetime 
from datetime import datetime
import os
day = datetime.today()
print(day.strftime("%d/%m"))
def counting():
  now = datetime.now()
  import time
  current_time = now.strftime("%H:%M:%S")
  while (True):
    print("Current Time is :", current_time, end="\r")
    time.sleep(0.1)
    nit = "18:38"
    if nit in current_time:
      print("nice")
    counting()
os.system("python time_counting.py")
