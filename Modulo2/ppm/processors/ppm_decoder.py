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
        self.k_def = k_max
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
        for letra in self.alphabet:
            self.structure[-1]["NO_CONTEXT"].add_character(letra)
        ## self.structure[-1]["NO_CONTEXT"].add_character("_")

    def get_context(self, k: int, context_str: str) -> Context:
        """Retorna o contexto para um determinado k e string de contexto."""
        context_key = context_str if context_str else "NO_CONTEXT"
        if context_key not in self.structure[k]: # Se não existe o contexto, cria um novo
            self.structure[k][context_key] = Context()
        return self.structure[k][context_key]
    
    def decode_sequence(self, encoded_data: str) -> str:
        """Decodifica uma sequência de bits concatenada."""
        context_stack = []
        cursor = 0
        decoded_text = ""
        num_chars = len(self.alphabet) + 1 ## +1 para o espaço
        x_bits = math.ceil(math.log2(num_chars))
        data = encoded_data[cursor:x_bits]
        _ , decoded_char = decodificar_ppm(self.structure, -1, "NO_CONTEXT", data, {}, False)
    
        if not decoded_char:
            raise ValueError("Erro ao decodificar o contexto")
        
        context = self.get_context(-1, "NO_CONTEXT")
        context.remove_character(decoded_char)
        
        self.get_context(0, "NO_CONTEXT").add_character(decoded_char)
        self.get_context(0, "NO_CONTEXT").add_character(self.esc_symbol)
        
        context_stack.append(decoded_char)
        decoded_text += decoded_char
        
        print(f"Contexto: {context_stack}")
        k_max = min(len(context_stack), self.k_def)
        restart_k = True
        
        cursor = x_bits

        found_char = False
        k = k_max
        
        ignore_chars = set()
        tamanho_codigo = len(encoded_data)
        cursor_end = cursor + 1
        while not found_char:
            bit_atual = encoded_data[cursor:cursor_end]
            if k > 0:
                context_str = ''.join(context_stack[-1:-(k+1):-1])
            else:
                context_str = "NO_CONTEXT"
            context = self.get_context(k, context_str)
            if len(context.char_counts) > 0:
                _ , decoded_char = decodificar_ppm(self.structure, k, context_str, bit_atual, self.ignore_chars, False)
                if decoded_char == None:
                    if k == -1:
                        cursor_end += 1
                        k = k_max
                    else:   
                        cursor_end += 1
                        
                if decoded_char == 'ç':
                    bit_atual = ''
                    # aux_dict = {c: count for c, count in context.char_counts.items() if c not in self.ignore_chars}
                    k_max = k - 1
                    cursor = cursor_end
                    cursor_end = cursor + 1
                    k-=1
                elif decoded_char != None:
                    
                    k_max = min(len(context_stack)+1, self.k_def) 
                    if k == -1:
                        context.remove_character(decoded_char)
                        k+=1
                    while k <= k_max:
                        if k > 0:
                            context_str = ''.join(context_stack[-1:-(k+1):-1])
                        else:
                            context_str = "NO_CONTEXT"
                        context = self.get_context(k, context_str)
                        context.add_character(decoded_char)
                        context.add_character(self.esc_symbol)
                        k += 1
                        
                    context_stack.append(decoded_char)
                    bit_atual = ''
                    ignore_chars.clear()
                    cursor = cursor_end
                    cursor_end= cursor + 1
                    k = k_max
            else:
                k-=1
        # while k >= -1:
        #     if k > 0:
        #         context_str = ''.join(context_stack[k-1::-1])
        #     else:
        #         context_str = "NO_CONTEXT"
        #     context = self.get_context(k, context_str)
        #     if len(context.char_counts) > 0:
                
        #         _ , decoded_char = decodificar_ppm(self.structure, k, context_str, bit_atual, self.ignore_chars, False)
        #         if decoded_char:
                    
                        
                    
                
                
                
                
