### Code for find the shortest route to shop

import json
import requests
import time
import os
import argparse
from util import Queue, room_graph
from dotenv import load_dotenv

load_dotenv()

parser = argparse.ArgumentParser(description='find the room provided at the command line')

parser.add_argument("room_number", help="The room number to find")

args = parser.parse_args()

room_number = int(args.room_number)

token = os.getenv('token')
current_room = requests.get(
    ' https://lambda-treasure-hunt.herokuapp.com/api/adv/init/',
    headers={
        'Authorization': 'Token ' + token},
).json()


def bfs():
    q = Queue()
    q.enqueue([current_room["room_id"]])
    print(q.size(), q.queue)
    visited = set()
    while q.size() > 0:
        path = q.dequeue()
        print(path)
        v = path[-1]
        if v not in visited:
            if v == room_number:
                return path

            visited.add(v)
            for key, value in room_graph[f'{v}'].items():
                new_path = list(path)
                new_path.append(value)
                q.enqueue(new_path)


route_to_shop = bfs()

print(route_to_shop)

result_route = []

for index in range(len(route_to_shop)):
    for direction in ["n", "e", "w", "s"]:
        try:
            if room_graph[f"{route_to_shop[index]}"][direction] == route_to_shop[index + 1]:
                result_route.append(direction)
        except KeyError:
            None
        except IndexError:
            None

counter = 0

while current_room["room_id"] != room_number:
    for direction in result_route:
        counter += 1
        time.sleep(current_room["cooldown"])
        new_room = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/',
                                 json={'direction': f'{direction}',
                                       "next_room_id": f'{route_to_shop[counter]}'},
                                 headers={'Authorization': 'Token ' + token}).json()
        current_room = new_room
        print(current_room)
