def get_parameters():
    simulation_time = int(input("Digite o tempo total de simulação (Minutos): "))
    Lambda = int(input("Digite a taxa de chegada de clientes: "))
    mu = int(input("Digite a taxa de serviço: "))
    rho = Lambda/mu
    return simulation_time, Lambda, mu, rho

def main():
    total_time, Lambda, mu, rho = get_parameters()

if __name__ == "__main__":
    main()