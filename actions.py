import requests
import time
import random
from proof import Proof
from timeit import default_timer as timer
import hashlib
from player import Player

base_url = 'https://lambda-treasure-hunt.herokuapp.com/api'


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
            proof = random.getrandbits(32)

        print("Proof found: " + str(proof) + " in " + str(timer() - start))
        self.new_proof = proof

    def valid_proof(self, last_proof, proof, difficulty):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:difficulty] == '0' * difficulty

    def mine(self, new_proof):
        x = int(new_proof)
        response = response = requests.post(self.base_url + '/bc/mine/',
                                            headers={'Authorization': self.player.token}, json={'proof': new_proof})
        try:
            data = response.json()
            time.sleep(data["cooldown"])
            return data
        except ValueError:
            print("Error: Non-json response")
            print("Response returned:")
            print(response)
            return
        # cooldown =  max(0, ())
        print("Response:", data)

    def get_last_proof(self):
        response = requests.get(self.base_url + '/bc/last_proof/',
                                headers={'Authorization': self.player.token})
        try:
            data = response.json()
        except ValueError:
            print(self.player.token)
            print("Error: Non-json response")
            print("Response returned:")
            print(response)
            return
        self.last_proof = Proof(data.get('proof'), data.get('difficulty'), data.get('cooldown'), data.get('messages'),
                                data.get('errors'))
        timer = time.time() + float(data.get('cooldown'))
        cooldown = max(0, (timer - time.time())) + 0.01
        time.sleep(cooldown)
        print("Response:", data)
        return data


myself = Player()

action = Actions(myself)

while True:
    # Get the last proof from the server
    last_proof = action.get_last_proof()
    action.proof_work(last_proof['proof'], last_proof['difficulty'])
    coin = action.mine(action.new_proof)
    print(coin)
    # if data.get('message') == 'New Block Forged':
    #     coins_mined += 1
    #     print("Total coins mined: " + str(coins_mined))
    # else:
    #     print(data.get('message'))
