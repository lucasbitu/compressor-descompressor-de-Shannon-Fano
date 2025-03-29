from typing import List, Any

from models.ppm_model import PPMModel

class PPMProcessor:
    """Gerencia o processamento do texto usando o modelo PPM."""
    
    def __init__(self, k_max: int = 2):
        self.model = PPMModel(k_max)
        self.discarded_chars = []  # Pilha de caracteres
        self.encoded_sequence = []  # Sequência codificada
    
    def process_text(self, text: str) -> List[Any]:
        """Processa o texto completo e retorna a sequência codificada."""
        for char in text:
            self.process_character(char)
        return self.encoded_sequence
    
    def process_character(self, char: str) -> None:
        """Processa um único caractere."""
        # Processa o caractere no modelo
        self.model.process_character(char, self.discarded_chars)
        
        # Atualiza a pilha de caracteres descartados
        self.discarded_chars.insert(0, char)
    
        print("array descartados ")
        print(self.discarded_chars)
        
        # Limpa os caracteres ignorados
        self.model.ignore_chars.clear()
        
        # Aqui você pode adicionar lógica para atualizar a sequência codificada
        # self.encoded_sequence.append(algum_valor) 