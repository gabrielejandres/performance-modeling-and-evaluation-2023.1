def get_parameters():
    initial_state = int(input("Digite a quantidade inicial de dinheiro a ser apostada: "))
    p = int(input("Digite a probabilidade de ganhar em cada tentativa: "))
    q = 1 - p
    return initial_state, p, q

def main():
    i, p, q = get_parameters()

if __name__ == "__main__":
    main()