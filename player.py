import requests
import time
import os
from dotenv import load_dotenv
load_dotenv()

try:
  base_url = 'https://lambda-treasure-hunt.herokuapp.com/api'
  token  = os.getenv('token')
except:
  print("Please set both BASE_URL and TOKEN in env file")

if token == '' or token is None:
  print('Invalid token')

class Player:
  def __init__(self):
    self.token = 'Token ' + token
    self.next_time_for_action = time.time()