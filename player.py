import requests

try:
  base_url = '<base_url>'
  token  = '<token>'
except:
  print("Please set both BASE_URL and TOKEN in env file")

if token == '' or token is None:
  print('Invalid token')

class Player:
  def __init__(self):
    self.token = 'Token' + token