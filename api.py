import flask
from flask import request
import redis

app = flask.Flask("name")

r = redis.Redis(
    host='redis-16763.c241.us-east-1-4.ec2.cloud.redislabs.com',
    port=16763,
    username='test',
    password='*J7p6!#*mC')

# http://127.0.0.1:5000/people?start=123&end=456&range=hourly
@app.route('/people', methods=['GET'])
def getPeople():
    start = request.args.get('start', type = int)
    end = request.args.get('end', type = int)
    range_ = request.args.get('range', type = str)

    # check if start, end, or range are null
    if start is None or end is None or range is None:
        return flask.jsonify({"error": "Please provide a start, end, and range"}), 400

    print("Start: " + str(start))
    print("End: " + str(end))
    print("Range: " + str(range))

    if range_ == "minutely":
        bucket_size = 60
    elif range_ == "hourly":
        bucket_size = 60*60
    elif range_ == "daily":
        bucket_size = 60*60*24
    elif range_ == "monthly":
        bucket_size = 60*60*24*30
    elif range_ == "yearly":
        bucket_size = 60*60*24*365
    # should aggregation type be "first", "avg", or what? which count should we report?
    result = r.ts().range('count', start, end, aggregation_type="first", bucket_size_msec=bucket_size)

    jsonout = []
    
    for i in range(len(result)):
        jsonout.append({"timestamp": result[i][0], "count": result[i][1]})

    # return sample json
    return flask.jsonify(jsonout), 200

# can be tested in postman
# http://127.0.0.1:5000/threshold?range=minutely&threshold=16
@app.route('/threshold', methods=['POST'])
def postThreshold():
    range_ = request.args.get('range', type = str)
    threshold = request.args.get('threshold', type = int)

    if range_ is None or threshold is None:
        return flask.jsonify({"error": "Please provide a range and a threshold"}), 400
    
    print("Range: " + str(range_))
    print("Threshold: " + str(threshold))

    r.hset("Thresholds", range_, threshold)

    jsonout = []
    # return sample json
    return flask.jsonify(jsonout), 200


app.run()