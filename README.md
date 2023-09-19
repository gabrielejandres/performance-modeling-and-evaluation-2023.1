#TODO

## About M/M/1
This code is a Python simulation of a single-server queueing system, specifically a M/M/1 queue. The M/M/1 notation represents a queue with exponential inter-arrival times and exponential service times, both characterized by rates Lambda (arrival rate) and mu (service rate), respectively. The code performs the following steps:

1. The user is prompted to enter the total simulation time, arrival rate (Lambda), and service rate (mu). The utilization factor (rho), which is the ratio of Lambda to mu, is calculated and printed to the console.

2. The code initializes the simulation clock to 0, the number of customers in the system to 0, and the number of customers served to 0.

3. It generates the first arrival time and the first departure time based on exponential distributions. The next event is determined by comparing these times. If the first arrival time occurs first, the next departure time is set to infinity, and vice versa.

4. The code simulates the queueing system over the specified time period. It checks if the next event is an arrival or a departure and updates the clock, the number of customers in the system, and the event times accordingly. The simulation continues until the clock exceeds the total simulation time, and the number of customers served and the number of customers in the system are returned.

5. The simulation is run for 100 rounds, and the average number of customers served and the average number of customers in the system are calculated and printed to the console.

6. The `main` function is called to start the simulation.

7. The utilization factor (rho) is printed to the console.

8. The code ends.

In summary, this code simulates a basic single-server queueing system and calculates statistics such as the average number of customers served and the average number of customers in the system over multiple simulation rounds. The utilization factor is also calculated and displayed to help analyze the system's performance.