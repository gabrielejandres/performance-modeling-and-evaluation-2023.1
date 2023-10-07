"""
    * Modelagem e Avaliação de Desempenho - UFRJ - 2023.2
    * Simulação dos cenários descritos no item 4 do trabalho
"""

from metrics import *

SIMULATION_TIME = 100


def print_scenario_information(scenario, Lambda, mu, simulation_time = SIMULATION_TIME):
    print(f"-------------- CASO {scenario} --------------")
    calculate_metrics(Lambda, mu, simulation_time, scenario)


if __name__ == "__main__":
    print_scenario_information(scenario=1, Lambda=1, mu=2) # Cenario 1
    print_scenario_information(scenario=2, Lambda=2, mu=4) # Cenario 2
    print_scenario_information(scenario=3, Lambda=1.05, mu=1) # Cenario 3
    print_scenario_information(scenario=4, Lambda=1.10, mu=1) # Cenario 4