"""
    * Modelagem e Avaliação de Desempenho - UFRJ - 2023.2
    * Simulação dos cenários descritos no item 4 do trabalho
"""

from metrics import *

SIMULATION_TIME = 100


def print_scenario_information(scenario, Lambda, mu, simulation_time = SIMULATION_TIME):
    print(f"-------------- CASO {scenario} --------------")
    print(f"λ = {Lambda} & μ = {mu}")
    mean_customers_per_round, mean_waiting_time_per_round, frac_times_on_zero_per_round = run_simulation(simulation_time, Lambda, mu)

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

    if scenario == 1 or scenario == 2:
        print("Média do número de clientes no sistema: ", mean_customers_on_system)
        print("-> Intervalo de confiança correspondente: ", confidence_interval_customers_on_system)
        print("Média do tempo de espera: ", mean_waiting_time)
        print("-> Intervalo de confiança correspondente: ", confidence_interval_waiting_time)
        print("CDF do número de clientes no sistema: ") # TODO
        print("CDF do tempo de espera no sistema: ") # TODO
        
    print("Fração de vezes que o sistema atinge o estado 0: ", mean_frac_times_on_zero) # TODO
    print("-> Intervalo de confiança correspondente: ", confidence_interval_frac_times_on_zero)
    print("--------------------------------\n")


if __name__ == "__main__":
    print_scenario_information(scenario=1, Lambda=1, mu=2) # Cenario 1
    print_scenario_information(scenario=2, Lambda=2, mu=4) # Cenario 2
    print_scenario_information(scenario=3, Lambda=1.05, mu=1) # Cenario 3
    print_scenario_information(scenario=4, Lambda=1.10, mu=1) # Cenario 4