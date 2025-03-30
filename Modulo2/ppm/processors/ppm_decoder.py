from typing import List, Dict, Tuple, Any
from models.ppm_model import PPMModel
from models.context import Context
from utils.encoder import decodificar_ppm
import math

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
        self.alphabet = "abcdr"
        ## self.alphabet = string.ascii_lowercase
        self.initialize_alphabet()
    
    def initialize_alphabet(self):
        """Inicializa o alfabeto para k=-1, igual ao modelo."""
        self.structure[-1]["NO_CONTEXT"] = Context()
        for letra in "abcdr":
            self.structure[-1]["NO_CONTEXT"].add_character(letra)
        ## self.structure[-1]["NO_CONTEXT"].add_character("_")
    
    
    def decode_sequence(self, encoded_data: str) -> str:
        """Decodifica uma sequência de bits concatenada."""
        context_stack = []
        k_def = self.k_max
        num_chars = len(self.alphabet) + 1 ## +1 para o espaço
        x_bits = math.ceil(math.log2(num_chars))
        encoded_data = encoded_data[0:x_bits]
        decoded_data = decodificar_ppm(self.structure, -1, "NO_CONTEXT", encoded_data, {}, False)
        if not decoded_data:
            raise ValueError("Erro ao decodificar o contexto")
        
        print(f"Contexto: {context_stack}")
            
        for bit in encoded_data[x_bits:]:
                
                
