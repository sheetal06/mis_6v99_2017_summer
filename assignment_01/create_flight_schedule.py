#creating flight schedule
import operator
from collections import OrderedDict

flights = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6']#List of flights
Airports = ['AUS', 'DAL', 'HOU']#List of Airports
flight_transit = {'AUS': {'DAL': 50, 'HOU': 45},
                 'DAL': {'HOU' :65, 'AUS':50},
                 'HOU':{'AUS':45 ,'DAL':65}}#dictionary for journey times
final_schedule = []
dep_starttime = 360#flight starting time
arrival_endtime = 1320#flights ending time
gates = {'AUS': 1, 'DAL': 2, 'HOU': 3}# dictionary for no. of gate sin each airport
ground_time = {'AUS' : 25 , 'DAL' : 30 , 'HOU' : 35}# dictionary for ground times in min
present_flights = {'AUS': 0, 'DAL': 0, 'HOU': 0}# starting with 0
austin_recent = []
dallas_recent = []
houston_recent = []
flights_used = []
flights_loc = {}
dept_flights = {}
gates_aus = {'1': []}
gates_dal = {'1': [], '2': []}
gates_hou = {'1': [], '2': [], '3': []}

# class for schedule objects
class Flight_schedule():
    def __init__(self) :
        self.startpoint = None
        self.endpoint = None
        self.flight_no = None
        self.starttime = None
        self.arrivaltime = None
        
# Method that creates initial schedule
def initial_schedule():
    global flights_used
    local_gates = gates.copy()
    local_gates = OrderedDict(sorted(local_gates.items(), reverse=True))
    for loc in local_gates.keys():
        num_iterations = gates[loc]  ## tracks the number of gates to schedule
        while (num_iterations > 0):
            avail_airports = [x for x in Airports if x != loc]
            for item in avail_airports:  # for each item loops and checks if there are any gates available for endpoint
                if (local_gates[item] > 0):
                    f = Flight_schedule()
                    f.flight_no = [x for x in flights if x not in flights_used][0]
                    f.startpoint = loc
                    f.endpoint = item
                    f.starttime = dep_starttime
                    f.arrivaltime = f.starttime + flight_transit[f.startpoint][f.endpoint]
                    if (f.endpoint == 'AUS'):
                        flights_loc[f.flight_no] = 'AUS'
                        gates_aus['1'] = [f.arrivaltime, f.arrivaltime + ground_time['AUS']]
                        dept_flights[f.flight_no] = f.arrivaltime + ground_time['AUS']
                    elif (f.endpoint == 'DAL'):
                        flights_loc[f.flight_no] = 'DAL'
                        gates_dal[[k for (k, v) in gates_dal.items() if len(v) == 0][0]] = [f.arrivaltime,
                                                                                            f.arrivaltime + ground_time[
                                                                                                'DAL']]
                        dept_flights[f.flight_no] = f.arrivaltime + ground_time['DAL']
                    else:
                        flights_loc[f.flight_no] = 'HOU'
                        gates_hou[[k for (k, v) in gates_hou.items() if len(v) == 0][0]] = [f.arrivaltime,
                                                                                            f.arrivaltime + ground_time[
                                                                                                'HOU']]
                        dept_flights[f.flight_no] = f.arrivaltime + ground_time['HOU']
                    present_flights[f.endpoint] += 1
                    local_gates[f.endpoint] -= 1
                    flights_used.append(f.flight_no)
                    final_schedule.append(f)
                    break
            num_iterations -= 1
