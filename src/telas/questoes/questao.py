import pygame

class Questao:
    def __init__(self, enunciado, opcoes, resposta_correta):
        self.enunciado = enunciado
        self.opcoes = opcoes
        self.resposta_correta = resposta_correta
    
    def wrap_text(self, text, font, max_width):
            lines = []
            for paragraph in text.split('\n'):
                words = paragraph.split(' ')
                if not words:
                    lines.append('')
                    continue
                line = words[0]
                for word in words[1:]:
                    test_line = line + ' ' + word
                    if font.size(test_line)[0] <= max_width:
                        line = test_line
                    else:
                        lines.append(line)
                        line = word
                lines.append(line)
            return lines

    def verificar_resposta(self, resposta):
        return resposta == self.resposta_correta