""" Solutions for https://adventofcode.com/2020/day/13 """

# import standard library modules used below.
from collections import UserList
from math import floor

# import third-party modules used below.
from sympy.ntheory.modular import crt


# Part 1: In the provided data file, what is the ID of the earliest bus to the
# airport multiplied by the number of minutes waiting?


# Create data model for output "bus schedule" in data file.
class BusSchedule(UserList):
    """ Data Model for bus schedule from data file """

    @classmethod
    def from_str(cls, input_str, dlm=','):
        """ Read bus schedule from specified file """
        return cls(v for v in input_str.split(dlm))

    def find_next_departure_times_from(self, timestamp):
        """ Find earliest possible departure time are specified timestamp """
        departure_times = {}
        for bus in self:
            if bus.isdigit():
                bus_number = int(bus)
                quotient = floor(timestamp / bus_number)
                departure_times[bus] = (quotient + 1) * bus_number
        return departure_times

    def find_departure_time_for_part2(self):
        """ Solve specified system of congruences using CRT """
        moduli = []
        congruences = []
        for i, bus in enumerate(self):
            if bus.isdigit():
                moduli.append(int(bus))
                congruences.append(-1*i)
        return crt(moduli, congruences, check=False)[0]

# Read waiting start time and "bus schedule" values from data file.
with open('data/day13_shuttle_search-data.txt') as fp:
    waiting_start_time = int(fp.readline().rstrip())
    bus_schedule = BusSchedule.from_str(fp.readline().rstrip())

# Find wait time and bus taken for Part 1.
bus_options = bus_schedule.find_next_departure_times_from(waiting_start_time)
departure_time = min(bus_options.values())
wait_time = departure_time - waiting_start_time
bus_taken = dict(map(reversed, bus_options.items()))[departure_time]
print(
    f'Number of in-service buses in data file: '
    f'{len([v for v in bus_schedule if v != "x"])}'
)
print(f'Bus taken for Part 1: {bus_taken}')
print(f'Earliest bus departure time for Part 1: {departure_time}')
print(
    f'Total wait time for Part 1: '
    f'{departure_time}-{waiting_start_time}={wait_time}')
print(
    f'Request product for for Part 1: '
    f'{int(bus_taken)}*{wait_time}={int(bus_taken)*wait_time}'
)


# Part 2: What is the earliest timestamp such that all of the listed bus IDs
# depart at offsets matching their positions in the list?


# Find timestamp for Part 2.
print(
    f'Request timestamp for for Part 2: '
    f'{bus_schedule.find_departure_time_for_part2()}'
)
