# This code is a Python simulation of a queueing system, specifically a single-server queue with arrivals and departures following exponential distributions. The code is used to model and analyze the behavior of this queueing system over a specified time period with multiple rounds of simulation. Here's a breakdown of what the code does:

# Imports the numpy package, which is used to generate random numbers from an exponential distribution.
import numpy as np


# 1. The user is prompted to enter the total simulation time, the arrival rate, and the service rate. The code then calculates the utilization factor (rho) and prints it to the console.
def get_parameters():
    simulation_time = int(input("Digite o tempo total de simulação (minutos): "))
    Lambda = int(input("Digite a taxa de chegada de clientes (lambda): "))
    mu = int(input("Digite a taxa de serviço (mi): "))
    rho = Lambda/mu
    return simulation_time, Lambda, mu, rho

# 2. The code then initializes the simulation clock to 0, the number of customers in the system to 0, and the number of customers served to 0.
def initialize():
    clock = 0
    num_in_system = 0
    num_served = 0
    return clock, num_in_system, num_served

# 3. The code then generates the first arrival time and the first departure time. The first arrival time is generated by drawing a random number from an exponential distribution with a mean of 1/lambda. The first departure time is generated by drawing a random number from an exponential distribution with a mean of 1/mu. The code then compares the first arrival time and the first departure time to determine which event occurs first. If the first arrival time occurs first, the code sets the next departure time to infinity. If the first departure time occurs first, the code sets the next arrival time to infinity.
def generate_first_event(Lambda, mu):
    first_arrival_time = np.random.exponential(1/Lambda)
    first_departure_time = np.random.exponential(1/mu)
    if first_arrival_time < first_departure_time:
        next_arrival_time = first_arrival_time
        next_departure_time = float('inf')
    else:
        next_arrival_time = float('inf')
        next_departure_time = first_departure_time
    return next_arrival_time, next_departure_time

# 4. The code then simulates the queueing system over the specified time period. The code first checks to see if the next event is an arrival or a departure. If the next event is an arrival, the code updates the simulation clock to the next arrival time, increments the number of customers in the system by 1, and generates the next arrival time and the next departure time. If the next event is a departure, the code updates the simulation clock to the next departure time, increments the number of customers served by 1, and generates the next arrival time and the next departure time. The code then checks to see if the simulation clock has exceeded the total simulation time. If the simulation clock has not exceeded the total simulation time, the code repeats the process of checking to see if the next event is an arrival or a departure. If the simulation clock has exceeded the total simulation time, the code returns the number of customers served and the number of customers in the system.
def simulate(simulation_time, Lambda, mu):
    clock, num_in_system, num_served = initialize()
    next_arrival_time, next_departure_time = generate_first_event(Lambda, mu)
    while clock < simulation_time:
        if next_arrival_time < next_departure_time:
            clock = next_arrival_time
            num_in_system += 1
            next_arrival_time += np.random.exponential(1/Lambda)
            if num_in_system == 1:
                next_departure_time = clock + np.random.exponential(1/mu)
        else:
            clock = next_departure_time
            num_in_system -= 1
            num_served += 1
            if num_in_system > 0:
                next_departure_time = clock + np.random.exponential(1/mu)
            else:
                next_departure_time = float('inf')
    return num_served, num_in_system

# 5. The code then runs the simulation for 100 rounds and calculates the average number of customers served and the average number of customers in the system over the 100 rounds. The code then prints the average number of customers served and the average number of customers in the system to the console.
def run_simulation(simulation_time, Lambda, mu):
    num_served_list = []
    num_in_system_list = []
    for i in range(100):
        num_served, num_in_system = simulate(simulation_time, Lambda, mu)
        num_served_list.append(num_served)
        num_in_system_list.append(num_in_system)
    avg_num_served = np.mean(num_served_list)
    avg_num_in_system = np.mean(num_in_system_list)
    print("Average number served: " + str(avg_num_served))
    print("Average number in system: " + str(avg_num_in_system))

# 6. The code then runs the simulation.
def main():
    total_time, Lambda, mu, rho = get_parameters()
    run_simulation(total_time, Lambda, mu)
    print("Utilization factor: " + str(rho)) # 7. The code then prints the utilization factor to the console.

# 8. The code then ends.
if __name__ == "__main__":
    main()