"""
    * Modelagem e Avaliação de Desempenho - UFRJ - 2023.2
    * Simulação de Fila M/M/1
"""

import numpy as np
from event import Event, EventType
import heapq


def initialize():
    """ Inicializa as variáveis da simulação """
    elapsed_time = 0 # tempo atual decorrido 
    customers_on_system = 0 # clientes no sistema no momento
    customers_served = 0 # clientes que ja foram atendidos
    customers_queue = [] # fila de eventos
    customers_arrived = 0 # numero de clientes que chegaram no sistema
    area = 0 # area do grafico de clientes no sistema x tempo para usar a lei de little
    last_event_time = 0 # tempo do ultimo evento
    times_on_zero = 0 # quantidade de vezes em zero
    total_events = 0 # quantidade total de eventos
    arrival_instants = [] # instantes de chegada dos clientes
    waiting_density = {} # desidade do tempo de espera
    number_clients_density = {} # densidade do numero de clientes no sistema

    return elapsed_time, customers_on_system, customers_served, customers_queue, customers_arrived, area, last_event_time, times_on_zero, total_events, arrival_instants, waiting_density, number_clients_density


def generate_first_event(Lambda):
    """ Gera o primeiro evento de chegada """
    first_arrival_time = np.random.exponential(1/Lambda) # escolhe um número da distribuição exponencial com media 1/lambda para ser o tempo da primeira chegada
    first_event = Event(EventType.ARRIVAL, first_arrival_time) # cria um evento de chegada com o tempo da primeira chegada
    return first_event 


def simulate_queue(simulation_time, Lambda, mu):
    """ Simula a fila M/M/1 """
    elapsed_time, customers_on_system, customers_served, customers_queue, customers_arrived, area, last_event_time, times_on_zero, total_events, arrival_instants, waiting_density, number_clients_density = initialize()

    # Gerar um evento inicial de chegada
    initial_event = generate_first_event(Lambda)

    # Adicionar esse evento inicial na fila
    heapq.heappush(customers_queue, initial_event)

    # Começar o loop da simulação (enquanto tempo atual for menor que o tempo total de simulação)
    while elapsed_time <= simulation_time:
        event = heapq.heappop(customers_queue)
        total_events += 1

        # Interrompe o loop se o tempo do evento for posterior ao final da simulação
        if event.time > simulation_time: 
            break
        
        # print(event)
        
        # atualiza a densidade do numero de clientes no sistema
        number_clients_density[customers_on_system] = number_clients_density.get(customers_on_system, 0) + 1

        # se o evento for um evento de chegada
        if event.type == EventType.ARRIVAL: 
            elapsed_time = event.time # tempo atual recebe o tempo do evento
            arrival_instants.append(elapsed_time) # adiciona o tempo de chegada do cliente na lista de tempos de chegada
            area += customers_on_system * (elapsed_time - last_event_time) # area recebe o numero de clientes no sistema multiplicado pelo tempo que eles ficaram no sistema
            customers_arrived += 1 # incrementa o numero de clientes que chegaram no sistema
            customers_on_system += 1 # incrementa o numero de clientes no sistema
            last_event_time = elapsed_time # atualiza o tempo do ultimo evento
            next_arrival_time = elapsed_time + np.random.exponential(1/Lambda) # escolhe um numero da distribuição exponencial com media 1/lambda para ser o tempo da proxima chegada
            next_arrival_event = Event(EventType.ARRIVAL, next_arrival_time) # cria um evento de chegada com o tempo da proxima chegada
            heapq.heappush(customers_queue, next_arrival_event) # adiciona o evento de chegada na fila de eventos

            # se o cliente que chegou for o ultimo na fila
            if customers_on_system == 1: 
                service_time = np.random.exponential(1/mu) # escolhe um numero da distribuição exponencial com media 1/mu para ser o tempo de atendimento
                next_departure_time = elapsed_time + service_time # tempo da proxima partida é o tempo atual mais o tempo de atendimento
                next_departure_event = Event(EventType.DEPARTURE, next_departure_time) # cria um evento de partida com o tempo da proxima partida
                heapq.heappush(customers_queue, next_departure_event) # adiciona o evento de partida na fila de eventos
            
        # se o evento for um evento de saida   
        elif event.type == EventType.DEPARTURE: 
            elapsed_time = event.time # tempo atual recebe o tempo do evento
            area += customers_on_system * (elapsed_time - last_event_time) # area recebe o numero de clientes no sistema multiplicado pelo tempo que eles ficaram no sistema
            customers_on_system -= 1 # decrementa o numero de clientes no sistema
            last_event_time = elapsed_time # atualiza o tempo do ultimo evento

            truncated_waiting_time = round(elapsed_time - arrival_instants[customers_served], 2) # tempo de espera do cliente que acabou de sair do sistema
            waiting_density[truncated_waiting_time] = waiting_density.get(truncated_waiting_time, 0) + 1 # atualiza a densidade do tempo de espera
            customers_served += 1 # incrementa o numero de clientes que foram atendidos
            
            # só adiciona um evento de partida se não for o último cliente a sair do sistema
            if customers_on_system > 0: 
                service_time = np.random.exponential(1/mu) # escolhe um numero da distribuição exponencial com media 1/mu para ser o tempo de atendimento
                next_departure_time = elapsed_time + service_time # tempo da proxima partida é o tempo atual mais o tempo de atendimento
                next_departure_event = Event(EventType.DEPARTURE, next_departure_time) # cria um evento de partida com o tempo da proxima partida
                heapq.heappush(customers_queue, next_departure_event) # adiciona o evento de partida na fila de eventos
        
            # se o próximo evento é saída e havia apenas um cliente no sistema
            if customers_on_system == 0:
                times_on_zero += 1



    # print(customers_arrived, area)
    return area, customers_arrived, times_on_zero/total_events, waiting_density, number_clients_density