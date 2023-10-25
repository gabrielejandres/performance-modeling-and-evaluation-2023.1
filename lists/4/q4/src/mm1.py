"""
    * Modelagem e Avaliação de Desempenho - UFRJ - 2023.2
    * Simulação de Fila M/M/1
"""

import numpy as np
from event import Event, EventType
import heapq

SPECIAL_CUSTOMER = 2001


def initialize():
    """ Inicializa as variáveis da simulação """
    elapsed_time = 0 # tempo atual decorrido 
    customers_on_system = 0 # clientes no sistema no momento
    customers_served = 0 # clientes que ja foram atendidos
    customers_queue = [] # fila de eventos
    customers_arrived = 0 # numero de clientes que chegaram no sistema

    return elapsed_time, customers_on_system, customers_served, customers_queue, customers_arrived


def generate_first_event(Lambda):
    """ Gera o primeiro evento de chegada """
    first_arrival_time = np.random.exponential(1/Lambda) # escolhe um número da distribuição exponencial com media 1/lambda para ser o tempo da primeira chegada
    first_event = Event(EventType.ARRIVAL, first_arrival_time) # cria um evento de chegada com o tempo da primeira chegada
    return first_event 


def simulate_queue(simulation_time, Lambda, mu, max_width):
    """ Simula a fila M/M/1 """
    elapsed_time, customers_on_system, customers_served, customers_queue, customers_arrived = initialize()
    queue_is_infinite = not max_width

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

        # se o evento for um evento de chegada
        if event.type == EventType.ARRIVAL: 
            elapsed_time = event.time # tempo atual recebe o tempo do evento
            next_arrival_time = elapsed_time + np.random.exponential(1/Lambda) # escolhe um numero da distribuição exponencial com media 1/lambda para ser o tempo da proxima chegada
            next_arrival_event = Event(EventType.ARRIVAL, next_arrival_time) # cria um evento de chegada com o tempo da proxima chegada
            heapq.heappush(customers_queue, next_arrival_event) # adiciona o evento de chegada na fila de eventos
            
            # Aceita novos clientes se a fila for infinita ou se o numero de clientes no sistema for menor que o tamanho maximo da fila
            if queue_is_infinite or customers_on_system < max_width:
                customers_arrived += 1 # incrementa o numero de clientes que chegaram no sistema
                customers_on_system += 1 # incrementa o numero de clientes no sistema

                if customers_arrived == SPECIAL_CUSTOMER:
                    initial_waiting_time = elapsed_time
                
            # se o cliente que chegou for o ultimo na fila
            if customers_on_system == 1: 
                service_time = np.random.exponential(1/mu) # escolhe um numero da distribuição exponencial com media 1/mu para ser o tempo de atendimento
                next_departure_time = elapsed_time + service_time # tempo da proxima partida é o tempo atual mais o tempo de atendimento
                next_departure_event = Event(EventType.DEPARTURE, next_departure_time) # cria um evento de partida com o tempo da proxima partida
                heapq.heappush(customers_queue, next_departure_event) # adiciona o evento de partida na fila de eventos
            
        # se o evento for um evento de saida   
        elif event.type == EventType.DEPARTURE: 
            elapsed_time = event.time # tempo atual recebe o tempo do evento
            customers_on_system -= 1 # decrementa o numero de clientes no sistema
            customers_served += 1 # incrementa o numero de clientes que foram atendidos

            if customers_served == SPECIAL_CUSTOMER:
                return elapsed_time - initial_waiting_time
            
            # só adiciona um evento de partida se não for o último cliente a sair do sistema
            if customers_on_system > 0: 
                service_time = np.random.exponential(1/mu) # escolhe um numero da distribuição exponencial com media 1/mu para ser o tempo de atendimento
                next_departure_time = elapsed_time + service_time # tempo da proxima partida é o tempo atual mais o tempo de atendimento
                next_departure_event = Event(EventType.DEPARTURE, next_departure_time) # cria um evento de partida com o tempo da proxima partida
                heapq.heappush(customers_queue, next_departure_event) # adiciona o evento de partida na fila de eventos