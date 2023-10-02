"""
    * Modelagem e Avaliação de Desempenho - UFRJ - 2023.2
    * Simulação de Fila M/M/1 um número "infinito" de vezes para obtermos as métricas de interesse
"""

import sys
from mm1 import *

INFINITY = 1000


def run_simulation(simulation_time, Lambda, mu):
    """ Simula infinitas rodadas e calcula a media de clientes e do tempo de espera em cada uma delas"""
    mean_customers_per_round = []
    mean_waiting_time_per_round = []    
    
    for _ in range(INFINITY):
        area, customers_arrived = simulate_queue(simulation_time, Lambda, mu)
        mean_customers_per_round.append(area/simulation_time)
        mean_waiting_time_per_round.append(area/customers_arrived)

    return mean_customers_per_round, mean_waiting_time_per_round


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


# TODO
def get_CDF():
    return 1


def main(simulation_time, Lambda, mu):
    print(f"λ = {Lambda} & μ = {mu}")
    mean_customers_per_round, mean_waiting_time_per_round = run_simulation(simulation_time, Lambda, mu)

    mean_customers_on_system = get_mean(mean_customers_per_round)
    variance_customers_on_system = get_variance(mean_customers_per_round, mean_customers_on_system)
    sd_customers_on_system = np.sqrt(variance_customers_on_system)
    confidence_interval_customers_on_system = get_confidence_interval(sd_customers_on_system, mean_customers_on_system, len(mean_customers_per_round))

    mean_waiting_time = get_mean(mean_waiting_time_per_round)
    variance_waiting_time = get_variance(mean_waiting_time_per_round, mean_waiting_time)
    sd_waiting_time = np.sqrt(variance_waiting_time)
    confidence_interval_waiting_time = get_confidence_interval(sd_waiting_time, mean_waiting_time, len(mean_waiting_time_per_round))

    print("Média do número de clientes no sistema: ", mean_customers_on_system)
    print("-> Intervalo de confiança correspondente: ", confidence_interval_customers_on_system)
    print("Média do tempo de espera: ", mean_waiting_time)
    print("-> Intervalo de confiança correspondente: ", confidence_interval_waiting_time)

    # rho = Lambda/mu
    # print("Utilization factor: " + str(rho)) 

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 mm1.py <simulation_time> <lambda> <mu>")
        exit(1)

    simulation_time = float(sys.argv[1])
    Lambda = float(sys.argv[2])
    mu = float(sys.argv[3])

    main(simulation_time=simulation_time, Lambda=Lambda, mu=mu)