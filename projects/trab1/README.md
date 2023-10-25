# Modelagem e Avaliação de Desempenho| 2023.2
*Implementação da fila M/M/1 e extração de métricas com a ruína do apostador.*

## Tabela de Conteúdo

1. [Tecnologias utilizadas](#tecnologias-utilizadas)
2. [Estrutura do repositório](#estrutura-do-repositório)
3. [Como rodar o código?](#como-rodar-o-codigo)
4. [Autores](#autores)

## 🖥️ Tecnologias utilizadas
O projeto foi desenvolvido utilizando a linguagem Python.
* Para a representação e criação de filas de prioridade, foi utilizado o módulo ```heapq```.
* Para realizar a escolha dos tempos dos eventos com distribuição exponencial, foi utilizado o pacote ```numpy```.
* Para a plotagem de gráficos, foi utilizada a biblioteca ```matplotlib```.

## 📂 Estrutura do repositório
O repositório está dividido em dois diretórios principais: _src_ e _aux_. O diretório aux contém os arquivos responsáveis pela plotagem dos gráficos e pelos resultados analíticos. O diretório _src_, por sua vez, contém os arquivos responsáveis pela implementação da M/M/1, extração de métricas e avaliação dos cenários solicitados no enunciado do trabalho.
* *aux/analytical.py*: Responsável pelo cálculo de métricas analíticas para o modelo M/M/1 e para a ruína do apostador
* *aux/graphics.py*: Responsável pela plotagem dos gráficos
* *src/event.py*: Responsável pela criação de eventos para o simulador de fila M/M/1
* *src/mm1.py*: Responsável pela simulação de fila M/M/1
* *src/metrics.py*: Responsável pela realização da simulação da fila M/M/1 um número "infinito" de rodadas para obtermos as métricas de interesse
* *src/scenarios.py*: Responsável pela simulação dos cenários descritos no item 4 do trabalho

## 📜 Como rodar o código?

1.  Clone esse repositório:
```
  git clone https://github.com/gabrielejandres/performance-modeling-and-evaluation-2023.1
```

2.  Para rodar os casos de teste do enunciado, primeiramente mude para o diretório *src*:
```
  cd src
```

3.  Execute o arquivo dos cenários:
```
  python3 scenarios.py
```
Essa execução irá gerar os resultados para todos os casos solicitados para filas infinitas e finitas.

4.  Caso deseje realizar a simulação para outros valores de λ e μ, é possível utilizando o arquivo de métricas:
```
  python3 metrics.py <simulation_time> <lambda> <mu>
```

## 👩‍💻 Autores
* Carlos Henrique Bravo Serrado
* Gabriele Jandres Cavalcanti
* Iago Rafael Lucas Martins
* Markson de Viana Arguello
* Victor Wohlers Cardoso
