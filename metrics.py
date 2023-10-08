"""
    * Modelagem e Avaliação de Desempenho - UFRJ - 2023.2
    * Simulação de Fila M/M/1 um número "infinito" de vezes para obtermos as métricas de interesse
"""

import sys
from mm1 import *
from graphics import *
from analytical import *

ROUNDS = 100
DEFAULT_SCENARIO = 0

def run_simulation(simulation_time, Lambda, mu, max_width):
    """ Simula infinitas rodadas e calcula as metricas em cada uma delas"""
    mean_customers_per_round = []
    mean_waiting_time_per_round = []
    frac_times_on_zero_per_round = []
    busy_times_per_round = []
    probability_reach_zero = []
    waiting_density = {}
    number_clients_density = {}
    reach_0_before_max_per_round = []
    
    for _ in range(ROUNDS):
        area, customers_arrived, frac_times_on_zero, frac_busy_times, waiting_density, number_clients_density, reach_0_before_max = simulate_queue(simulation_time, Lambda, mu, max_width)
        mean_customers_per_round.append(area/simulation_time)
        # mean_waiting_time_per_round.append(area/customers_arrived - 1/mu) # se fóssemos calcular só o tempo de espera, descontamos o tempo de serviço para que calculemos só o tempo de espera, desconsideramos o tempo de serviço
        mean_waiting_time_per_round.append(area/customers_arrived) 
        frac_times_on_zero_per_round.append(frac_times_on_zero)
        busy_times_per_round.append(frac_busy_times)
        probability_reach_zero.append(1) if frac_times_on_zero > 0 else probability_reach_zero.append(0)
        reach_0_before_max_per_round.append(reach_0_before_max)

    return mean_customers_per_round, mean_waiting_time_per_round, busy_times_per_round, frac_times_on_zero_per_round, waiting_density, number_clients_density, probability_reach_zero, reach_0_before_max_per_round


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

    
def calculate_metrics(Lambda, mu, simulation_time, max_width, scenario = DEFAULT_SCENARIO):
    print(f"λ = {Lambda} & μ = {mu}")
    mean_customers_per_round, mean_waiting_time_per_round, frac_times_on_zero_per_round, frac_busy_times_per_round, waiting_density, number_clients_density, probability_reach_zero, reach_0_before_max_per_round = run_simulation(simulation_time, Lambda, mu, max_width)

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

    mean_prob_reach_zero = get_mean(probability_reach_zero)
    variance_prob_reach_zero = get_variance(probability_reach_zero, mean_prob_reach_zero)
    sd_prob_reach_zero = np.sqrt(variance_prob_reach_zero)
    confidence_interval_prob_reach_zero = get_confidence_interval(sd_prob_reach_zero, mean_prob_reach_zero, len(probability_reach_zero))

    mean_prob_go_zero_before_max  = get_mean(reach_0_before_max_per_round)
    variance_prob_go_zero_before_max = get_variance(reach_0_before_max_per_round, mean_prob_go_zero_before_max)
    sd_prob_go_zero_before_max = np.sqrt(variance_prob_go_zero_before_max)
    confidence_interval_prob_go_zero_before_max = get_confidence_interval(sd_prob_go_zero_before_max, mean_prob_go_zero_before_max, len(reach_0_before_max_per_round))

    if scenario in (DEFAULT_SCENARIO, 1, 2):
        print("\n-- Média do número de clientes no sistema --")
        print("Simulação: ", mean_customers_on_system)
        print("Intervalo de confiança correspondente -> ", confidence_interval_customers_on_system)
        print("Analítico (Lei de Little): ", get_mean_customers_on_system_by_littles_law(Lambda, mu))

        print("\n-- Média do tempo de espera (tempo de espera = tempo na fila de espera + tempo de serviço) --")
        print("Simulação: ", mean_waiting_time)
        print("Intervalo de confiança correspondente -> ", confidence_interval_waiting_time)
        print("Analítico: ", get_mean_response_time_by_mm1_formula(Lambda, mu))

        print("\n-- CDF do número de clientes no sistema --") 
        plot_cdf_number_clients(number_clients_density, Lambda, mu)

        print("\n-- CDF do tempo de espera no sistema --") 
        plot_cdf_waiting_time(waiting_density, Lambda, mu)

        print("")

    if scenario in (DEFAULT_SCENARIO, 3, 4):
        print("\n-- Fração de períodos ocupados finitos: --")
        print("Simulação:", mean_busy_times)
        print("Intervalo de confiança correspondente ->", confidence_interval_busy_times)
        if Lambda < mu: # se o regime de serviço for conservado, podemos usar a fórmula da M/M/1
            print("Analítico:", get_mean_busy_times_by_mm1_formula(Lambda, mu)) 
        else:
            print("Analítico: ", "Não é possível calcular pois λ > μ")
        
    print("\n-- Fração de vezes que o sistema atinge o estado 0 (Probabilidade de estar em 0 no regime estacionário) --")
    print("Simulação: ", mean_frac_times_on_zero) 
    print("Intervalo de confiança correspondente ->", confidence_interval_frac_times_on_zero)
    if Lambda < mu: # se o regime de serviço for conservado, podemos usar a fórmula da M/M/1
        print("Analítico (Fórmula M/M/1): ", get_frac_times_on_i_by_mm1_formula(Lambda, mu, 0))
    else:
        print("Analítico: ", "Não é possível calcular pois λ > μ")
    
    if not(max_width): # fila infinita
        print("\n-- Probabilidade de esvaziar (alcançar 0), dado que começou em 1 --")
        print("Simulação: ", mean_prob_reach_zero) 
        print("Intervalo de confiança correspondente ->", confidence_interval_prob_reach_zero)
        print("Analítico (Ruína do Apostador): ", get_prob_reach_zero_by_gamblers_ruin(Lambda, mu, 1))
    else: # fila finita
        print("\n-- Probabilidade de esvaziar antes de estourar, dado que começou em 1 --")
        print("Simulação: ", mean_prob_go_zero_before_max) 
        print("Intervalo de confiança correspondente ->", confidence_interval_prob_go_zero_before_max)
        print("Analítico (Ruína do Apostador): ", get_prob_reach_zero_by_gamblers_ruin_finite(Lambda, mu, max_width, 1)) # se a fila for finita, podemos usar a fórmula da ruína do apostador

    print("\n-----------------------------------\n")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 mm1.py <simulation_time> <lambda> <mu>")
        exit(1)

    simulation_time = float(sys.argv[1])
    Lambda = float(sys.argv[2])
    mu = float(sys.argv[3])

    calculate_metrics(Lambda=Lambda, mu=mu, simulation_time=simulation_time)