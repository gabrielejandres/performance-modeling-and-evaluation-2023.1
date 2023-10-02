"""
    * Modelagem e Avaliação de Desempenho - UFRJ - 2023.2
    * Simulação dos cenários descritos no item 4 do trabalho
"""

from mm1 import *

SIMULATION_TIME = 100

def print_scenario_information(scenario, Lambda, mu, simulation_time = SIMULATION_TIME):
    print(f"-------------- CASO {scenario} --------------")
    print(f"λ = {Lambda} & μ = {mu}")
    mean_customers_per_round, mean_waiting_time_per_round = get_means_per_round(simulation_time, Lambda, mu)

    mean_customers_on_system = get_mean(mean_customers_per_round)
    variance_customers_on_system = get_variance(mean_customers_per_round, mean_customers_on_system)
    sd_customers_on_system = np.sqrt(variance_customers_on_system)
    confidence_interval_customers_on_system = get_confidence_interval(sd_customers_on_system, mean_customers_on_system, len(mean_customers_per_round))

    mean_waiting_time = get_mean(mean_waiting_time_per_round)
    variance_waiting_time = get_variance(mean_waiting_time_per_round, mean_waiting_time)
    sd_waiting_time = np.sqrt(variance_waiting_time)
    confidence_interval_waiting_time = get_confidence_interval(sd_waiting_time, mean_waiting_time, len(mean_waiting_time_per_round))

    if scenario == 1 or scenario == 2:
        print("Média do número de clientes no sistema: ", mean_customers_on_system)
        print("-> Intervalo de confiança correspondente: ", confidence_interval_customers_on_system)
        print("Média do tempo de espera: ", mean_waiting_time)
        print("-> Intervalo de confiança correspondente: ", confidence_interval_waiting_time)
        print("CDF do número de clientes no sistema: ") # TODO
        print("CDF do tempo de espera no sistema: ") # TODO
        
    print("Fração de vezes que o sistema atinge o estado 0: ") # TODO
    print("--------------------------------\n")

def first_scenario():
    Lambda = 1
    mu = 2
    print_scenario_information(1, Lambda, mu)

def second_scenario():
    Lambda = 2
    mu = 4
    print_scenario_information(2, Lambda, mu)

def third_scenario():
    Lambda = 1.05
    mu = 1
    print_scenario_information(3, Lambda, mu)

def fourth_scenario():
    Lambda = 1.10
    mu = 1
    print_scenario_information(4, Lambda, mu)

first_scenario()
second_scenario()
third_scenario()
fourth_scenario()