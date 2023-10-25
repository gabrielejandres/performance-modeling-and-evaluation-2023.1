"""
    * Modelagem e Avaliação de Desempenho - UFRJ - 2023.2
    * Simulação de Fila M/M/1 em várias rodadas para obtermos as métricas de interesse
"""

import sys
sys.path.append('../')
 
from mm1 import *
from aux.analytical import *

ROUNDS = 200

def run_simulation(simulation_time, Lambda, mu, max_width):
    """ Simula as rodadas e calcula a media do tempo de espera do cliente especifico em cada uma delas"""
    mean_waiting_time_per_round = []
    
    for _ in range(ROUNDS):
        waiting_time_last_customer = simulate_queue(simulation_time, Lambda, mu, max_width)
        mean_waiting_time_per_round.append(waiting_time_last_customer)

    return mean_waiting_time_per_round


def get_mean(mean_per_round):
    """ Obtem a media de uma distribuição """
    return np.mean(mean_per_round)


def get_variance(mean_per_round, mean_on_system):
    """ Obtem a variancia de uma distribuição """
    customers_on_system_variance = 0
    for mean in mean_per_round:
        customers_on_system_variance += pow(mean - mean_on_system, 2) / max(len(mean_per_round) - 1, 1)
    return customers_on_system_variance


def get_confidence_interval(standard_deviation, sample_mean, sample_size):
    """ Calcula o intervalo de confiança """
    lowest_point = sample_mean - 1.96 * (standard_deviation / np.sqrt(sample_size))
    highest_point = sample_mean + 1.96 * (standard_deviation / np.sqrt(sample_size))
    
    return (lowest_point, highest_point)

    
def calculate_metrics(Lambda, mu, simulation_time, max_width = None):
    print(f"λ = {Lambda} & μ = {mu}")
    mean_waiting_time_per_round = run_simulation(simulation_time, Lambda, mu, max_width)

    mean_waiting_time = get_mean(mean_waiting_time_per_round)
    variance_waiting_time = get_variance(mean_waiting_time_per_round, mean_waiting_time)
    sd_waiting_time = np.sqrt(variance_waiting_time)
    confidence_interval_waiting_time = get_confidence_interval(sd_waiting_time, mean_waiting_time, len(mean_waiting_time_per_round))

    print("\n-- Média do tempo de espera (tempo de espera = tempo na fila de espera + tempo de serviço) --")
    print("Simulação: E(T) = ", mean_waiting_time)
    print(f"Intervalo de confiança correspondente -> [{confidence_interval_waiting_time[0]}, {confidence_interval_waiting_time[1]}]")
    print("Analítico: E(T) = ", get_analytical_waiting_time(Lambda, mu))

    print("\n------------------------------------\n")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 metrics.py <simulation_time> <lambda> <mu>")
        exit(1)

    simulation_time = float(sys.argv[1])
    Lambda = float(sys.argv[2])
    mu = float(sys.argv[3])

    calculate_metrics(Lambda = Lambda, mu = mu, simulation_time = simulation_time)