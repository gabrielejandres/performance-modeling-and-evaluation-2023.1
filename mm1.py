"""
    * Modelagem e Avaliação de Desempenho - UFRJ - 2023.2
    * Simulação de Fila M/M/1
"""
import sys
import numpy as np
from event import Event, EventType
import heapq

INFINITY = 30

def initialize():
    """ Inicializa as variáveis da simulação """
    elapsed_time = 0 # tempo atual decorrido 
    customers_in_system = 0 # clientes no sistema no momento
    customers_served = 0 # clientes que ja foram atendidos
    customers_queue = [] # fila de eventos
    customers_arrived = 0 # numero de clientes que chegaram no sistema
    area = 0 # area do grafico de clientes no sistema x tempo para usar a lei de little
    last_event_time = 0 # tempo do ultimo evento

    return elapsed_time, customers_in_system, customers_served, customers_queue, customers_arrived, area, last_event_time


def generate_first_event(Lambda):
    """ Gera o primeiro evento de chegada """
    first_arrival_time = np.random.exponential(1/Lambda) # escolhe um número da distribuição exponencial com media 1/lambda para ser o tempo da primeira chegada
    first_event = Event(EventType.ARRIVAL, first_arrival_time) # cria um evento de chegada com o tempo da primeira chegada
    return first_event 

def simulate(simulation_time, Lambda, mu):
    """ Simula a fila M/M/1 """
    elapsed_time, customers_in_system, customers_served, customers_queue, customers_arrived, area, last_event_time = initialize()

    # Gerar um evento inicial de chegada
    initial_event = generate_first_event(Lambda)

    # Adicionar esse evento inicial na fila
    heapq.heappush(customers_queue, initial_event)

    # Começar o loop da simulação (enquanto tempo atual for menor que o tempo total de simulação)
    while elapsed_time <= simulation_time:
        event = heapq.heappop(customers_queue)

        # Interrompe o loop se o tempo do evento for posterior ao final da simulação
        if event.time > simulation_time: 
            break
        
        # print(event)

        # se o evento for um evento de chegada
        if event.type == EventType.ARRIVAL: 
            elapsed_time = event.time # tempo atual recebe o tempo do evento
            area += customers_in_system * (elapsed_time - last_event_time) # area recebe o numero de clientes no sistema multiplicado pelo tempo que eles ficaram no sistema
            customers_arrived += 1 # incrementa o numero de clientes que chegaram no sistema
            customers_in_system += 1 # incrementa o numero de clientes no sistema
            last_event_time = elapsed_time # atualiza o tempo do ultimo evento
            next_arrival_time = elapsed_time + np.random.exponential(1/Lambda) # escolhe um numero da distribuição exponencial com media 1/lambda para ser o tempo da proxima chegada
            next_arrival_event = Event(EventType.ARRIVAL, next_arrival_time) # cria um evento de chegada com o tempo da proxima chegada
            heapq.heappush(customers_queue, next_arrival_event) # adiciona o evento de chegada na fila de eventos

            # se o cliente que chegou for o primeiro da fila
            if customers_in_system == 1: 
                service_time = np.random.exponential(1/mu) # escolhe um numero da distribuição exponencial com media 1/mu para ser o tempo de atendimento
                next_departure_time = elapsed_time + service_time # tempo da proxima partida é o tempo atual mais o tempo de atendimento
                next_departure_event = Event(EventType.DEPARTURE, next_departure_time) # cria um evento de partida com o tempo da proxima partida
                heapq.heappush(customers_queue, next_departure_event) # adiciona o evento de partida na fila de eventos
            
        # se o evento for um evento de saida   
        elif event.type == EventType.DEPARTURE: 
            elapsed_time = event.time # tempo atual recebe o tempo do evento
            area += customers_in_system * (elapsed_time - last_event_time) # area recebe o numero de clientes no sistema multiplicado pelo tempo que eles ficaram no sistema
            customers_in_system -= 1 # decrementa o numero de clientes no sistema
            last_event_time = elapsed_time # atualiza o tempo do ultimo evento
            customers_served += 1 # incrementa o numero de clientes que foram atendidos
            
            # só adiciona um evento de partida se não for o último cliente a sair do sistema
            if customers_in_system > 0: 
                service_time = np.random.exponential(1/mu) # escolhe um numero da distribuição exponencial com media 1/mu para ser o tempo de atendimento
                next_departure_time = elapsed_time + service_time # tempo da proxima partida é o tempo atual mais o tempo de atendimento
                next_departure_event = Event(EventType.DEPARTURE, next_departure_time) # cria um evento de partida com o tempo da proxima partida
                heapq.heappush(customers_queue, next_departure_event) # adiciona o evento de partida na fila de eventos


    # print(customers_arrived, area)
    return area, customers_arrived
        
def get_expected_values(simulation_time, Lambda, mu):
    """ Calcula os valores esperados """
    mean_customers_per_round = []
    mean_waiting_time_per_round = []    
    
    for _ in range(INFINITY):
        area, customers_arrived = simulate(simulation_time, Lambda, mu)
        mean_customers_per_round.append(area/simulation_time)
        mean_waiting_time_per_round.append(area/customers_arrived)

    return np.mean(mean_customers_per_round), np.mean(mean_waiting_time_per_round)


# def confidence_interval(standard_deviation, sample_mean, sample_size):
#     """ Calcula o intervalo de confiança """
#     interval = {'lowEndPoint': 0, 'highEndPoint': 0}
    
#     interval['lowEndPoint'] = sample_mean - 1.96 * (standard_deviation / np.sqrt(sample_size))
#     interval['highEndPoint'] = sample_mean + 1.96 * (standard_deviation / np.sqrt(sample_size))
    
#     return interval


def main(simulation_time, Lambda, mu):
    mean_customers_on_system, mean_waiting_time = get_expected_values(simulation_time, Lambda, mu)
    print("Média do número de clientes no sistema: ", mean_customers_on_system)
    print("Média do tempo de espera: ", mean_waiting_time)
    # rho = Lambda/mu
    # print("Utilization factor: " + str(rho)) 

if __name__ == "__main__":
    # Obtem os parametros da simulação
    n = len(sys.argv)

    if n != 4:
        print("Usage: python3 mm1.py <simulation_time> <lambda> <mu>")
        exit(1)

    simulation_time = float(sys.argv[1])
    Lambda = float(sys.argv[2])
    mu = float(sys.argv[3])

    main(simulation_time=simulation_time, Lambda=Lambda, mu=mu)