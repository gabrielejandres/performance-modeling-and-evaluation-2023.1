"""
    * Modelagem e Avaliação de Desempenho - UFRJ - 2023.2
    * Criação de eventos para o simulador de fila M/M/1
"""

from enum import Enum

class EventType(Enum):
    ARRIVAL = 0
    DEPARTURE = 1

class Event:
    def __init__(self, type, time):
        self.type = type
        self.time = time
    
    def __lt__(self, other):
        return self.time < other.time
    
    def __str__(self):
        return f"{self.type} at {self.time}"
    
    def __eq__(self, other):
        return self.type == other.type and self.time == other.time
    
    def __hash__(self):
        return hash((self.type, self.time))
