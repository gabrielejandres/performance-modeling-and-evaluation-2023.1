"""
    * Modelagem e Avaliação de Desempenho - UFRJ - 2023.2
    * Cálculo de métricas analíticas para o modelo M/M/1
"""

# Lei de little para calcular a média de clientes no sistema
def get_mean_customers_on_system_by_littles_law(Lambda, mu):
    rho = Lambda/mu
    return rho / (1 - rho)
    
# Distribuição estacionária em i (probabilidade de estar em i) pela fórmula da M/M/1
def get_frac_times_on_i_by_mm1_formula(Lambda, mu, i):
    rho = Lambda/mu
    return (1 - rho) * pow(rho, i)

# Probabilidade de ser absorvido em 0 começando no estado k em uma fila FINITA
def get_prob_reach_zero_by_gamblers_ruin_finite(Lambda, mu, n, k):
    p = Lambda / (Lambda + mu)
    q = 1 - p

    if p == q:
        return 1 - k / n
        
    return 1 - (1 - pow(q/p, k))/(1 - pow(q/p, n))


# Probabilidade de alacançar o estado 0 em uma fila INFINITA
def get_prob_reach_zero_by_gamblers_ruin(Lambda, mu, k):
    if mu < Lambda:
        return pow(mu/Lambda, k)
    else:
        return 1.0