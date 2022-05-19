import redis
import time
from random import randint

class _ZedObjectData():
    def __init__(self, id):
        self.id = id
    def get_id(self):
        return self.id
    def update_id(self, id):
        self.id = id

z = _ZedObjectData(randint(100, 500))

sightings_array = []
for i in range(10):
    # uncomment this line and comment the other one for final use
    # sightings_array.append({"time": int(time.time()), "id": z.get_id()})
    sightings_array.append({"id": z.get_id()})
    z.update_id(randint(100, 500))

r = redis.Redis(
    host='redis-16763.c241.us-east-1-4.ec2.cloud.redislabs.com',
    port=16763,
    username='test',
    password='*J7p6!#*mC')

r.publish('channel', "Started new publisher instance")

while len(sightings_array) > 0:
    # add the data point to the timestream by incrementing the time's count 
    r.ts().add('count', int(time.time()), 1, duplicate_policy="sum")
    # publish the data point to the channel and delete it
    # not sure how to use this anymore since implementation changed
    r.publish('channel', str(sightings_array.pop(0)))

# {10002542142: 14}, {24142141331: 15}, {3214341341: 53}, {51: 1}