"""Companion code to https://realpython.com/simulation-with-simpy/
'Simulating Real-World Processes With SimPy'
Python version: 3.7.3
SimPy version: 3.0.11
"""

import simpy
import random
import statistics
import json

def init():
    pass

def run(input):

    input = json.loads(input)

    num_cashiers, num_servers, num_ushers = input['cashiers'], input['servers'], input['ushers']

    checks = [num_cashiers is None, num_servers is None, num_ushers is None]

    if any(checks):
        num_cashiers, num_servers, num_ushers = 1, 1, 1

    # Run the simulation
    env = simpy.Environment()
    wait_times = MonitoredResource(env, capacity=1)

    env.process(run_theater(env, wait_times, num_cashiers, num_servers, num_ushers))
    env.run(until = 90)

    # View the results
    mins, secs = calculate_wait_time(wait_times.data)

    output = {'minutes' : mins, 'seconds' : secs}

    output = json.dumps(output)

    return output

class MonitoredResource(simpy.Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = []

    def put(self, time):
        self.data.append(time)


class Theater(object):
    def __init__(self, env, num_cashiers, num_servers, num_ushers):
        self.env = env
        self.cashier = simpy.Resource(env, num_cashiers)
        self.server = simpy.Resource(env, num_servers)
        self.usher = simpy.Resource(env, num_ushers)

    def purchase_ticket(self, moviegoer):
        yield self.env.timeout(random.randint(1, 3))

    def check_ticket(self, moviegoer):
        yield self.env.timeout(3 / 60)

    def sell_food(self, moviegoer):
        yield self.env.timeout(random.randint(1, 5))

def go_to_movies(env, res, moviegoer, theater):
    # Moviegoer arrives at the theater
    arrival_time = env.now

    with theater.cashier.request() as request:
        yield request
        yield env.process(theater.purchase_ticket(moviegoer))

    with theater.usher.request() as request:
        yield request
        yield env.process(theater.check_ticket(moviegoer))

    if random.choice([True, False]):
        with theater.server.request() as request:
            yield request
            yield env.process(theater.sell_food(moviegoer))

    # Moviegoer heads into the theater
    res.put(env.now - arrival_time)

def run_theater(env, res, num_cashiers, num_servers, num_ushers):
    theater = Theater(env, num_cashiers, num_servers, num_ushers)

    for moviegoer in range(3):
        env.process(go_to_movies(env, res, moviegoer, theater))

    while True:
        yield env.timeout(0.20)  # Wait a bit before generating a new person

        moviegoer += 1
        env.process(go_to_movies(env, res, moviegoer, theater))

def calculate_wait_time(wait_times):
    average_wait = statistics.mean(wait_times)
    # Pretty print the results
    minutes, frac_minutes = divmod(average_wait, 1)
    seconds = frac_minutes * 60
    return round(minutes), round(seconds)