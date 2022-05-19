import redis

r = redis.Redis(
    host='redis-16763.c241.us-east-1-4.ec2.cloud.redislabs.com',
    port=16763,
    username='test',
    password='*J7p6!#*mC')

sub = r.pubsub()
sub.subscribe('channel')
print("Started new subscriber instance")

for message in sub.listen():
    if message is not None and isinstance(message, dict):
        data = message.get('data')
        if isinstance(data, bytes):
            data = data.decode('utf-8')
            print(data)