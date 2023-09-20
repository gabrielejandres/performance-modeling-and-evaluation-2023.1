import sys
import numpy as np
from event import Event, EventType
import heapq

INFINITY = 1

# Inicializa as estruturas de dados e variaveis de contagem
def initialize():
    elapsed_time = 0
    customers_in_system = 0
    customers_served = 0
    return elapsed_time, customers_in_system, customers_served

def generate_first_event(Lambda):
    first_arrival_time = np.random.exponential(1/Lambda) # escolhe um número da distribuição exponencial com media 1/lambda para ser o tempo da primeira chegada
    first_event = Event(EventType.ARRIVAL, first_arrival_time)
    return first_event

# Realiza uma simulacao
def simulate(simulation_time, Lambda, mu, debug=False):
    elapsed_time, customers_in_system, customers_served = initialize()

    # Gerar um evento inicial de chegada
    initial_event = generate_first_event(Lambda)

    # Adicionar esse evento inicial na fila
    customers_queue = []
    heapq.heappush(customers_queue, initial_event)

    # Começar o loop da simulação (enquanto tempo atual for menor que o tempo total de simulação)
    while elapsed_time < simulation_time:
        event = heapq.heappop(customers_queue)
        if event.time > simulation_time: 
            break
        if(debug): print(event)
        elapsed_time = event.time 

        # se o evento for um evento de chegada
        if event.type == EventType.ARRIVAL: 
            customers_in_system += 1
            next_arrival_time = elapsed_time + np.random.exponential(1/Lambda)
            next_arrival_event = Event(EventType.ARRIVAL, next_arrival_time)
            heapq.heappush(customers_queue, next_arrival_event)

            # se o cliente que chegou for o primeiro da fila
            if customers_in_system == 1: 
                service_time = np.random.exponential(1/mu)
                next_departure_time = elapsed_time + service_time
                next_departure_event = Event(EventType.DEPARTURE, next_departure_time) 
                heapq.heappush(customers_queue, next_departure_event)
            
        # se o evento for um evento de saida   
        elif event.type == EventType.DEPARTURE: 
            customers_in_system -= 1
            customers_served += 1
            
            # só adiciona um evento de partida se não for o último cliente a sair do sistema
            if customers_in_system > 0: 
                service_time = np.random.exponential(1/mu)
                next_departure_time = elapsed_time + service_time
                next_departure_event = Event(EventType.DEPARTURE, next_departure_time)
                heapq.heappush(customers_queue, next_departure_event)

    return customers_served, customers_in_system
        
        
def get_expected_value(simulation_time, Lambda, mu):
    customers_served_list = []
    customers_in_system_list = []
    
    for _ in range(INFINITY):
        customers_served, customers_in_system = simulate(simulation_time, Lambda, mu)
        customers_served_list.append(customers_served)
        customers_in_system_list.append(customers_in_system)

    avg_customers_served = np.mean(customers_served_list)
    avg_customers_in_system = np.mean(customers_in_system_list)

    return avg_customers_served, avg_customers_in_system

def main(simulation_time, Lambda, mu, debug=False):
    customers_served, customers_in_system = simulate(simulation_time, Lambda, mu, debug)
    print("Total number served: " + str(customers_served))
    print("Total number in system: " + str(customers_in_system))

    avg_customers_served, avg_customers_in_system = get_expected_value(simulation_time, Lambda, mu)
    print("Expected value of customers served: " + str(avg_customers_served))
    print("Expected value of customers in system: " + str(avg_customers_in_system))
    
    # rho = Lambda/mu
    # print("Utilization factor: " + str(rho)) 

if __name__ == "__main__":
    # Obtem os parametros da simulação
    n = len(sys.argv)
    if(n < 4 or n > 5):
        print("Usage: python3 mm1v2.py <simulation_time> <lambda> <mu> [debug]")
        exit(1)
    simulation_time = float(sys.argv[1])
    Lambda = float(sys.argv[2])
    mu = float(sys.argv[3])
    debug = False
    if(n == 5 and sys.argv[4] == "1"):
        debug = True
    main(simulation_time=simulation_time, Lambda=Lambda, mu=mu, debug=debug)