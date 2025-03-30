from typing import List, Dict, Tuple, Any
from models.ppm_model import PPMModel
from models.context import Context
from utils.encoder import huffman_encoding, equiprovable_huffman

class PPMDecoder:
    """Decodificador para o modelo PPM (Prediction by Partial Matching)."""
    
    def __init__(self, k_max: int = 2, verbose: bool = True):
        """
        Inicializa o decodificador PPM.
        """
        self.k_max = k_max
        self.verbose = verbose
        self.esc_symbol = 'ç'  # Símbolo de escape (ro)
        self.structure = {k: {} for k in range(-1, k_max + 1)}
        self.ignore_chars = set()
        self.discarded_chars = []
        self.initialize_alphabet()
    
    def initialize_alphabet(self):
        """Inicializa o alfabeto para k=-1, igual ao modelo."""
        self.structure[-1]["NO_CONTEXT"] = Context()
        for letra in "abcdr":
            self.structure[-1]["NO_CONTEXT"].add_character(letra)
    
    def decode_sequence(self, encoded_data: str) -> str:
        """Decodifica uma sequência de bits concatenada."""
        decoded_text = ""
        self.discarded_chars = []
        pos = 0
        
        while pos < len(encoded_data):
            # Decodifica o próximo caractere
            char, bits_used = self.decode_next_character(encoded_data[pos:])
            
            if char and bits_used > 0:
                if self.verbose:
                    print(f"Decodificado: '{char}' usando {bits_used} bits")
                
                # Se for um caractere normal (não escape), adiciona ao texto
                if char != self.esc_symbol:
                    decoded_text += char
                    # Atualiza pilha de contexto
                    self.discarded_chars.insert(0, char)
                    if len(self.discarded_chars) > self.k_max:
                        self.discarded_chars.pop()
                    
                    if self.verbose:
                        print(f"Texto atual: '{decoded_text}'")
                        print(f"Pilha de contexto: {self.discarded_chars}")
                else:
                    if self.verbose:
                        print(f"Encontrado símbolo de escape")
                
                # Atualiza o modelo com o caractere decodificado
                self.update_model(char)
                
                # Avança na string de bits
                pos += bits_used
                
                # Limpa caracteres ignorados
                self.ignore_chars = set()
            else:
                # Se não conseguiu decodificar, avança um bit
                pos += 1
                if self.verbose:
                    print(f"Não conseguiu decodificar na posição {pos-1}")
        
        return decoded_text
