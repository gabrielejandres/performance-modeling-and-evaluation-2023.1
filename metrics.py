"""
    * Modelagem e Avaliação de Desempenho - UFRJ - 2023.2
    * Simulação de Fila M/M/1 um número "infinito" de vezes para obtermos as métricas de interesse
"""

import sys
from mm1 import *
from graphics import plot_cdf_number_clients, plot_cdf_waiting_time

ROUNDS = 100


def run_simulation(simulation_time, Lambda, mu):
    """ Simula infinitas rodadas e calcula as metricas em cada uma delas"""
    mean_customers_per_round = []
    mean_waiting_time_per_round = []
    frac_times_on_zero_per_round = []
    busy_times_per_round = []
    waiting_density = {}
    number_clients_density = {}  
    
    for _ in range(ROUNDS):
        area, customers_arrived, frac_times_on_zero, frac_busy_times, waiting_density, number_clients_density = simulate_queue(simulation_time, Lambda, mu)
        mean_customers_per_round.append(area/simulation_time)
        mean_waiting_time_per_round.append(area/customers_arrived)
        frac_times_on_zero_per_round.append(frac_times_on_zero)
        busy_times_per_round.append(frac_busy_times)

    return mean_customers_per_round, mean_waiting_time_per_round, busy_times_per_round, frac_times_on_zero_per_round, waiting_density, number_clients_density


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


def plot_CDF(waiting_density, number_clients_density, Lambda, mu):
    plot_cdf_waiting_time(waiting_density, Lambda, mu)
    plot_cdf_number_clients(number_clients_density, Lambda, mu)

    
def calculate_metrics(Lambda, mu, simulation_time, scenario = 0):
    print(f"λ = {Lambda} & μ = {mu}")
    mean_customers_per_round, mean_waiting_time_per_round, frac_times_on_zero_per_round, frac_busy_times_per_round, waiting_density, number_clients_density = run_simulation(simulation_time, Lambda, mu)

    mean_customers_on_system = get_mean(mean_customers_per_round)
    variance_customers_on_system = get_variance(mean_customers_per_round, mean_customers_on_system)
    sd_customers_on_system = np.sqrt(variance_customers_on_system)
    confidence_interval_customers_on_system = get_confidence_interval(sd_customers_on_system, mean_customers_on_system, len(mean_customers_per_round))

    mean_waiting_time = get_mean(mean_waiting_time_per_round)
    variance_waiting_time = get_variance(mean_waiting_time_per_round, mean_waiting_time)
    sd_waiting_time = np.sqrt(variance_waiting_time)
    confidence_interval_waiting_time = get_confidence_interval(sd_waiting_time, mean_waiting_time, len(mean_waiting_time_per_round))

    mean_frac_times_on_zero = get_mean(frac_times_on_zero_per_round)
    variance_frac_times_on_zero = get_variance(frac_times_on_zero_per_round, mean_frac_times_on_zero)
    sd_frac_times_on_zero = np.sqrt(variance_frac_times_on_zero)
    confidence_interval_frac_times_on_zero = get_confidence_interval(sd_frac_times_on_zero, mean_frac_times_on_zero, len(frac_times_on_zero_per_round))

    mean_busy_times = get_mean(frac_busy_times_per_round)
    variance_busy_times = get_variance(frac_busy_times_per_round, mean_busy_times)
    sd_frac_busy_times = np.sqrt(variance_busy_times)
    confidence_interval_busy_times = get_confidence_interval(sd_frac_busy_times, mean_busy_times, len(frac_busy_times_per_round))

    if scenario in (0, 1, 2):
        print("Média do número de clientes no sistema: ", mean_customers_on_system)
        print("-> Intervalo de confiança correspondente: ", confidence_interval_customers_on_system)
        print("Média do tempo de espera: ", mean_waiting_time)
        print("-> Intervalo de confiança correspondente: ", confidence_interval_waiting_time)
        print("CDF do número de clientes no sistema: ") 
        plot_cdf_number_clients(number_clients_density, Lambda, mu)
        print("CDF do tempo de espera no sistema: ") 
        plot_cdf_waiting_time(waiting_density, Lambda, mu)

    if scenario in (0, 3, 4):
        print("Fração de períodos ocupados finitos: ", mean_busy_times)
        print("-> Intervalo de confiança correspondente: ", confidence_interval_busy_times)
        
    print("Fração de vezes que o sistema atinge o estado 0: ", mean_frac_times_on_zero) 
    print("-> Intervalo de confiança correspondente: ", confidence_interval_frac_times_on_zero)
    print("--------------------------------\n")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 mm1.py <simulation_time> <lambda> <mu>")
        exit(1)

    simulation_time = float(sys.argv[1])
    Lambda = float(sys.argv[2])
    mu = float(sys.argv[3])

    calculate_metrics(Lambda=Lambda, mu=mu, simulation_time=simulation_time)