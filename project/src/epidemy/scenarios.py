"""
    * Modelagem e Avaliação de Desempenho - UFRJ - 2023.2
    * Simulação dos cenários descritos no item 4 do trabalho
"""

from metrics import *

TOTAL_RUNS = 1000
SIZE_INITIAL_POPULATION = 1
MAX_GENERATIONS = 100

def print_scenario_information(scenario, mu, Lambda, is_deterministic = False, size_initial_population = SIZE_INITIAL_POPULATION, max_generations = MAX_GENERATIONS, total_runs = TOTAL_RUNS):
    print(f"\n-------------- CASO {scenario} --------------")
    generate_metrics(mu, Lambda, is_deterministic, size_initial_population, max_generations, total_runs)


if __name__ == "__main__":
    print("=============== Tempo de serviço exponencial ===============")
    print_scenario_information(scenario = 1, mu = 2, Lambda = 1) # Cenario 1
    print_scenario_information(scenario = 2, mu = 4, Lambda = 2) # Cenario 2
    print_scenario_information(scenario = 3, mu = 1, Lambda = 1.05) # Cenario 3
    print_scenario_information(scenario = 4, mu = 1, Lambda = 1.10) # Cenario 4

    # print("=============== Tempo de serviço determinístico ===============\n")
    # print_scenario_information(scenario = 1, mu = 2, Lambda = 1, is_deterministic = True) # Cenario 1
    # print_scenario_information(scenario = 2, mu = 4, Lambda = 2, is_deterministic = True) # Cenario 2
    # print_scenario_information(scenario = 3, mu = 1, Lambda = 1.05, is_deterministic = True) # Cenario 3
    # print_scenario_information(scenario = 4, mu = 1, Lambda = 1.10, is_deterministic = True) # Cenario 4