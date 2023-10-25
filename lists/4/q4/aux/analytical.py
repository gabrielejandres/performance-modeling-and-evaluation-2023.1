"""
    * Modelagem e Avaliação de Desempenho - UFRJ - 2023.2
    * Cálculo de métricas analíticas para o modelo M/M/1 
"""

# Média do tempo de espera de um cliente
def get_analytical_waiting_time(Lambda, mu):
    mean_service_time = 1/mu
    return mean_service_time/(1 - Lambda * mean_service_time)