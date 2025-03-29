import string
from typing import Dict, List

from models.context import Context
from utils.encoder import decodificar_ppm  # Importando a função

class PPMModel:
    """Modelo principal do PPM (Prediction by Partial Matching)."""
    
    def __init__(self, k_max: int = 2, verbose: bool = True):
        self.k_max = k_max
        self.structure = {k: {} for k in range(-1, k_max + 1)}
        self.ignore_chars = set()
        self.esc_symbol = 'ç'  # Símbolo de escape (ro)
        self.encoded_bits = []  # Lista para armazenar os bits codificados
        self.verbose = verbose
        self.initialize_alphabet()
    
    def initialize_alphabet(self):
        """Inicializa o modelo com o alfabeto para k=-1."""
        self.structure[-1]["NO_CONTEXT"] = Context()
        # Adiciona todas as letras minúsculas
        #for letra in string.ascii_lowercase:
        for letra in "abcdr":
            self.structure[-1]["NO_CONTEXT"].add_character(letra)
        # Adiciona o espaço
        # self.structure[-1]["NO_CONTEXT"].add_character("_")
    
    def get_context(self, k: int, context_str: str) -> Context:
        """Retorna o contexto para um determinado k e string de contexto."""
        context_key = context_str if context_str else "NO_CONTEXT"
        if context_key not in self.structure[k]: # Se não existe o contexto, cria um novo
            self.structure[k][context_key] = Context()
        return self.structure[k][context_key]
    
    def is_context_complete(self, context: Context) -> bool:
        """Verifica se um contexto contém todos os símbolos do alfabeto incluindo espaço."""
        # alphabet = set(string.ascii_lowercase)
        alphabet = set(["a", "b", "c", "d", "r"])
        # alphabet.add("_")  # Adiciona o espaço
        context_chars = context.get_characters()
        return alphabet.issubset(context_chars)
    
    
    def process_character(self, char: str, context_stack: List[str]) -> None:
        """Processa um caractere no modelo PPM."""
        element_found = False
        
        if not context_stack:
            # Caso especial para o primeiro caractere
            # Codifica o caractere no contexto -1
            encoded_bits = decodificar_ppm(self.structure, -1, "NO_CONTEXT", char, self.ignore_chars, False)
            if encoded_bits:
                self.encoded_bits.append((char, -1, "NO_CONTEXT", encoded_bits))
                if self.verbose:
                    print(f"Codificando '{char}' no contexto -1 com bits: {encoded_bits}")
            
            self.structure[-1]["NO_CONTEXT"].remove_character(char)
            self.get_context(0, "NO_CONTEXT").add_character(char)
            self.get_context(0, "NO_CONTEXT").add_character(self.esc_symbol)
        else:
            stack_size = len(context_stack)
            stack_size = min(stack_size, self.k_max)
            
            # Verifica cada nível de k, começando pelo maior possível
            for k in range(stack_size, -2, -1):
                if k > 0:
                    context_str = ''.join(context_stack[k-1::-1])
                else:
                    context_str = "NO_CONTEXT"
                
                context = self.get_context(k, context_str)
                
                if context.contains(char):
                    if k == -1:
                        # Codifica o caractere no contexto -1
                        encoded_bits = decodificar_ppm(self.structure, -1, "NO_CONTEXT", char, self.ignore_chars, False)
                        if encoded_bits:
                            self.encoded_bits.append((char, -1, "NO_CONTEXT", encoded_bits))
                            if self.verbose:
                                print(f"Codificando '{char}' no contexto -1 com bits: {encoded_bits}")
                        
                        context.remove_character(char)
                    else:
                        if not element_found:
                            # Codifica o caractere no contexto atual
                            encoded_bits = decodificar_ppm(self.structure, k, context_str, char, self.ignore_chars, False)
                            if encoded_bits:
                                self.encoded_bits.append((char, k, context_str, encoded_bits))
                                if self.verbose:
                                    print(f"Codificando '{char}' no contexto {k}:{context_str} com bits: {encoded_bits}")
                        
                        element_found = True
                        context.add_character(char)
                else:
                    if k != -1:
                        # Caracteres que devem ser ignorados na codificação
                        characters = {c for c in context.get_characters() if c != self.esc_symbol}
                        if self.verbose:
                            print(f"Contexto caracteres: {characters}")
                        
                        if characters:
                            self.ignore_chars.update(characters)
                        
                        if not element_found:
                            # Codifica o caractere de escape (ro)
                            escape_bits = decodificar_ppm(self.structure, k, context_str, self.esc_symbol, self.ignore_chars, False)
                            if escape_bits:
                                self.encoded_bits.append((self.esc_symbol, k, context_str, escape_bits))
                                if self.verbose:
                                    print(f"Codificando escape '{self.esc_symbol}' no contexto {k}:{context_str} com bits: {escape_bits}")
                        
                        # Adiciona escape symbol e o caractere
                        context.add_character(self.esc_symbol)
                        context.add_character(char)
                        
                        if self.is_context_complete(context):
                            context.remove_character(self.esc_symbol)
    
    def get_probabilities(self, context_str: str, k: int) -> Dict[str, float]:
        """Calcula as probabilidades para um dado contexto."""
        context = self.get_context(k, context_str)
        total_count = sum(context.char_counts.values())
        return {char: count / total_count for char, count in context.char_counts.items()}
    
    def get_encoded_bits(self) -> List:
        """Retorna os bits codificados até o momento."""
        return self.encoded_bits 