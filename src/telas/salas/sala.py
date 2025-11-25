
import pygame
import random
from src.utils.utils import questao_sequencial, questao_quiz

class Sala:

    def __init__(self, nome_sala, numero_sala):
        self.nome_sala = nome_sala
        self.numero_sala = numero_sala  
    
    def embaralha_questoes(self):
        indices_sequenciais = [self.numero_sala * 3 + i for i in range(3)]
        indices_quiz = [self.numero_sala * 2 + i for i in range(2)]
        
        questoes_sala = []
        for idx in indices_sequenciais:
            questoes_sala.append(questao_sequencial(idx))
        for idx in indices_quiz:
            questoes_sala.append(questao_quiz(idx))
        
        random.shuffle(questoes_sala)

        return questoes_sala
    