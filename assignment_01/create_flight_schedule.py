#creating flight schedule
import operator
from collections import OrderedDict

flights = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6']#List of flights
Airports = ['AUS', 'DAL', 'HOU']#List of Airports
flight_transit = {'AUS': {'DAL': 50, 'HOU': 45},
                 'DAL': {'HOU' :65, 'AUS':50},
                 'HOU':{'AUS':45 ,'DAL':65}}#dictionary for journey times
final_schedule = []
dep_departuretime = 360#flight starting time
arrival_endtime = 1320#flights ending time
gates = {'AUS': 1, 'DAL': 2, 'HOU': 3}# dictionary for no. of gate sin each airport
ground_time = {'AUS' : 25 , 'DAL' : 30 , 'HOU' : 35}# dictionary for ground times in min
present_flights = {'AUS': 0, 'DAL': 0, 'HOU': 0}# starting with 0
austin_recent = []
dallas_recent = []
houston_recent = []
flights_utilized = []
flights_port = {}
dept_flights = {}
Aus_gates = {'1': []}
Dal_gates = {'1': [], '2': []}
Hou_gates = {'1': [], '2': [], '3': []}

# class for schedule objects
class Flight_schedule():
    def __init__(self) :
        self.origin = None
        self.destination = None
        self.flight_no = None
        self.departuretime = None
        self.arrivaltime = None
        
# Method that creates initial schedule
def initial_schedule():
    global flights_utilized
    Airport_gates = gates.copy()
    Airport_gates = OrderedDict(sorted(Airport_gates.items(), reverse=True))
    for port in Airport_gates.keys():
        count = gates[port]  ## tracks the number of gates to schedule
        while (count > 0):
            avail_airports = [z for z in Airports if z != port]
            for place in avail_airports:  # for each item loops  
                if (Airport_gates[place] > 0):#checks if there are any gates available for destination
                    f = Flight_schedule()
                    f.flight_no = [z for z in flights if z not in flights_utilized][0]
                    f.origin = port
                    f.destination = place
                    f.departuretime = dep_departuretime
                    f.arrivaltime = f.departuretime + flight_transit[f.origin][f.destination]
                    if (f.destination == 'HOU'):#checking for Houston
                        flights_port[f.flight_no] = 'HOU'
                        Hou_gates[[m for (m, n) in Hou_gates.items() if len(n) == 0][0]] = [f.arrivaltime,
                                                                                            f.arrivaltime + ground_time[
                                                                                                'HOU']]
                        dept_flights[f.flight_no] = f.arrivaltime + ground_time['HOU']
                        
                    elif (f.destination == 'DAL'):#checking for Dallas
                        flights_port[f.flight_no] = 'DAL'
                        Dal_gates[[m for (m, n) in Dal_gates.items() if len(n) == 0][0]] = [f.arrivaltime,
                                                                                            f.arrivaltime + ground_time[
                                                                                                'DAL']]
                        dept_flights[f.flight_no] = f.arrivaltime + ground_time['DAL']
                    else:
                        flights_port[f.flight_no] = 'AUS'#checking for Austin
                        Aus_gates['1'] = [f.arrivaltime, f.arrivaltime + ground_time['AUS']]
                        dept_flights[f.flight_no] = f.arrivaltime + ground_time['AUS']
                        
                    present_flights[f.destination] += 1
                    Airport_gates[f.destination] -= 1
                    flights_utilized.append(f.flight_no)
                    final_schedule.append(f)
                    break
            count -= 1

# Method for converting time to military format
def convert_time(val):
    hrs = str(int(val/60))
    min = str(int(val)%60)
    return hrs.zfill(2)+min.zfill(2)

## method to continue the schedule.
def continue_schedule():
    free_gates = gates.copy()
    Airport_gates = gates.copy()
    filled_gates = {'AUS': 0, 'DAL': 0, 'HOU': 0}
    Airport_gates = OrderedDict(sorted(Airport_gates.items()))
    global flights_port
    global dept_flights
    flights_port = OrderedDict(sorted(flights_port.items()))
    for flight, port in flights_port.items(): ## for iterating over each flight after intital schedule
        avail_airports = [z for z in Airports if z != port]
        flag = False
        for avail_ports in avail_airports:
            if (avail_ports == 'HOU' and flag == False):# filling for Houston
                if (filled_gates[avail_ports] < Airport_gates[avail_ports]):
                    for gate, period in Hou_gates.items():
                        if (dept_flights[flight] > period[1]):
                            f = Flight_schedule()
                            f.flight_no = flight
                            f.origin = port
                            f.destination = avail_ports
                            f.departuretime = dept_flights[flight]
                            f.arrivaltime = f.departuretime + flight_transit[f.origin][f.destination]
                            if (f.arrivaltime <= 1320):
                                final_schedule.append(f)
                                dept_flights[f.flight_no] = f.arrivaltime + ground_time['HOU']
                                Hou_gates[gate] = [f.arrivaltime, f.arrivaltime + ground_time['HOU']]
                                filled_gates[f.destination] += 1
                                free_gates[f.origin] -= 1
                                flights_port[flight] = f.destination
                                flag = True
                                break
                            
            elif (avail_ports == 'DAL' and flag == False):#filling for Dallas
                if (filled_gates[avail_ports] < Airport_gates[avail_ports]):
                    for gate, period in Dal_gates.items():
                        if (dept_flights[flight] > period[1]):  ## Check before scheduling the flight for arrival time at destination
                            f = Flight_schedule()
                            f.flight_no = flight
                            f.origin = port
                            f.destination = avail_ports
                            f.departuretime = dept_flights[flight]
                            f.arrivaltime = f.departuretime + flight_transit[f.origin][f.destination]
                            if (f.arrivaltime <= 1320): ## append if only arrival time is less than constraint else loop through other destination
                                final_schedule.append(f)
                                dept_flights[f.flight_no] = f.arrivaltime + ground_time['DAL']
                                Dal_gates[gate] = [f.arrivaltime, f.arrivaltime + ground_time['DAL']]
                                filled_gates[f.destination] += 1
                                free_gates[f.origin] -= 1
                                flights_port[flight] = f.destination
                                flag = True
                                break
            elif (avail_ports == 'AUS' and flag == False):#filling for Austin
                if (filled_gates[avail_ports] < Airport_gates[avail_ports]):
                    for gate, period in Aus_gates.items():
                        if (dept_flights[flight] > period[1]):
                            f = Flight_schedule()
                            f.flight_no = flight
                            f.origin = port
                            f.destination = avail_ports
                            f.departuretime = dept_flights[flight]
                            f.arrivaltime = f.departuretime + flight_transit[f.origin][f.destination]
                            if (f.arrivaltime <= 1320):
                                dept_flights[f.flight_no] = f.arrivaltime + ground_time['AUS']
                                Aus_gates['1'] = [f.arrivaltime, f.arrivaltime + ground_time['AUS']]
                                final_schedule.append(f)
                                filled_gates[f.destination] += 1
                                free_gates[f.origin] -= 1
                                flights_port[flight] = f.destination
                                flag = True
                                break
        if (flag == False): ## If none of the above work, then find the gate with less dept time.
            port_flights_shrt = [m for m, n in flights_port.items() if n in avail_airports]
            dept_flights_shrt = dict([(m, n) for m, n in dept_flights.items() if m in port_flights_shrt])
            dept_flights_shrt = OrderedDict(sorted(dept_flights_shrt.items()))
            try:## Exceptional handling if there are no ports available.
                small_key = min(dept_flights_shrt, key=dept_flights_shrt.get)
            except ValueError:
                print(dept_flights_shrt, port_flights_shrt, flights_port, dept_flights, avail_airports)
            nearest_location = flights_port[small_key]
            f = Flight_schedule()
            f.flight_no = flight
            f.origin = port
            f.destination = nearest_location
            f.departuretime = dept_flights_shrt[small_key]
            f.arrivaltime = f.departuretime + flight_transit[f.origin][f.destination]
            if (f.arrivaltime <= 1320 and nearest_location == 'AUS'): ## append only if the conditions are met
                dept_flights[f.flight_no] = f.arrivaltime + ground_time['AUS']
                Aus_gates['1'] = [f.arrivaltime, f.arrivaltime + ground_time['AUS']]
                final_schedule.append(f)
                filled_gates[f.destination] += 1
                free_gates[f.origin] -= 1
                flights_port[flight] = f.destination
                flag = True
            elif (f.arrivaltime <= 1320 and nearest_location == 'DAL'):
                gate = [m for m, n in Dal_gates.items() if n[1] == dict(dept_flights_shrt)[small_key]][0]
                final_schedule.append(f)
                dept_flights[f.flight_no] = f.arrivaltime + ground_time['DAL']
                Dal_gates[gate] = [f.arrivaltime, f.arrivaltime + ground_time['DAL']]
                filled_gates[f.destination] += 1
                free_gates[f.origin] -= 1
                flights_port[flight] = f.destination
                flag = True
            elif (f.arrivaltime <= 1320 and nearest_location == 'HOU'):
                gate = [m for m, n in Hou_gates.items() if n[1] == dict(dept_flights_shrt)[small_key]]
                final_schedule.append(f)
                dept_flights[f.flight_no] = f.arrivaltime + ground_time['HOU']
                try: ## handling if there are no gates available.
                    Dal_gates[gate] = [f.arrivaltime, f.arrivaltime + ground_time['HOU']]
                except TypeError:
                    pass
                filled_gates[f.destination] += 1
                free_gates[f.origin] -= 1
                flights_port[flight] = f.destination
                flag = True
    return

## Method that calls the functions and printing csv file
if __name__ == "__main__":
    initial_schedule()
    while (True):
        ini_len = len(final_schedule) ## checks if there is any change in the schedule, if not breaks the while loop
        continue_schedule()
        if (ini_len == len(final_schedule)):
            break
    final_schedule.sort(key=operator.attrgetter("flight_no", "departuretime"), reverse=False) ## sort the final schedule in necessary order
    with open("flight_schedule.csv", 'w') as f:
        header = "flight_number,origin,destination,departure_time,arrival_time \n"
        f.write(header)
        for place in final_schedule:
            shrt = place.flight_no + "," + place.origin + "," + place.destination + "," + convert_time( place.departuretime) + "," + convert_time( place.arrivaltime) + '\n'
            f.write(shrt)
    f.close()
