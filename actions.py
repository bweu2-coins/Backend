import requests
from proof import Proof
from timeit import default_timer as timer
import hashlib

base_url = '<base_url>'

class Actions:
  def __init__(self, player):
    self.player = player
    self.base_url = base_url
    self.message = ''
    self.last_proof = Proof()
    self.new_proof = 0

  def proof_work(self, last_proof, difficulty):
    start = timer()
    print('Searching for next proof')
    print(last_proof)

    proof = 100000000
    while self.valid_proof(last_proof, proof, difficulty) is False:
        proof -= 1

    print("Proof found: " + str(proof) + " in " + str(timer() - start))
    self.new_proof = proof 

  def valid_proof(self, last_proof, proof, difficulty):
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:difficulty] == '0' * difficulty


  def mine(self, new_proof):
    response = response = requests.post(self.base_url + '/bc/mine/',
                                 headers={'Authorization': self.player.token}, json={'proof': int(new_proof)})

    try:
      data = response.json()
    except ValueError:
      print("Error: Non-json response")
      print("Response returned:")
      print(response)
      return
    # cooldown player, apply the cool down script
    print("Response:", data)

  def get_last_proof(self):
    response = requests.get(self.base_url + '/bc/last_proof/', 
                            headers={'Authorization': self.player.token})
    try:
      data = response.json()
    except ValueError:
      print("Error: Non-json response")
      print("Response returned:")
      print(response)
      return
    # cooldown player, apply the cool down script
    self.last_proof = Proof(data.get('proof'), data.get('difficulty'), data.get('cooldown'), data.get('mesage'), data.get('errors'))
    print("Response:", data)