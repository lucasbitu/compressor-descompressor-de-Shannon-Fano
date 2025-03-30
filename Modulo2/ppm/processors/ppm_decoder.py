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
    
    def decode_next_character(self, bits: str) -> Tuple[str, int]:
        """Decodifica o próximo caractere na sequência."""
        # Define o nível máximo de contexto baseado na pilha atual
        max_context = min(len(self.discarded_chars), self.k_max)
        
        # Tenta cada nível de contexto, do maior para o menor
        for k in range(max_context, -2, -1):
            # Obtém o contexto atual
            if k == -1:
                context_str = "NO_CONTEXT"
            elif k == 0:
                context_str = "NO_CONTEXT"
            else:
                context_str = ''.join(self.discarded_chars[:k])
            
            if self.verbose:
                print(f"Tentando decodificar no contexto {k}:{context_str}")
            
            # Verifica se o contexto existe
            if k >= 0 and context_str not in self.structure[k]:
                if self.verbose:
                    print(f"Criando novo contexto {k}:{context_str}")
                self.structure[k][context_str] = Context()
            
            # Gera os códigos para este contexto
            codes = self.generate_codes(k, context_str)
            
            if not codes:
                if self.verbose:
                    print(f"Sem códigos disponíveis para contexto {k}:{context_str}")
                continue
            
            # Tenta encontrar um código correspondente
            for code, char in codes.items():
                if bits.startswith(code):
                    if self.verbose:
                        print(f"Encontrou código '{code}' para '{char}' no contexto {k}:{context_str}")
                    
                    # Se for um escape, marca caracteres para ignorar
                    if char == self.esc_symbol and k >= 0:
                        context = self.structure[k][context_str]
                        self.ignore_chars.update(c for c in context.get_characters() if c != self.esc_symbol)
                    
                    return char, len(code)
        
        return "", 0
    
    def generate_codes(self, k: int, context_str: str) -> Dict[str, str]:
        """Gera códigos para um determinado contexto."""
        # Obtém o contexto
        if k == -1:
            context = self.structure[-1]["NO_CONTEXT"]
        else:
            context = self.structure[k][context_str]
        
        # Filtra caracteres ignorados
        char_counts = {c: count for c, count in context.char_counts.items() 
                      if c not in self.ignore_chars}
        
        if not char_counts:
            return {}
        
        # Gera os códigos
        if k == -1:
            codes = equiprovable_huffman(char_counts)
        else:
            codes = huffman_encoding(char_counts, False)
        
        # Inverte para facilitar a busca (código -> caractere)
        return {code: char for char, code in codes.items()}
    
    def update_model(self, char: str):
        """Atualiza o modelo PPM após decodificar um caractere."""
        # Atualiza contextos existentes com o novo caractere
        for k in range(min(len(self.discarded_chars), self.k_max), -1, -1):
            if k == -1 or k == 0:
                context_str = "NO_CONTEXT"
            else:
                context_str = ''.join(self.discarded_chars[:k])
            
            # Garante que o contexto existe
            if context_str not in self.structure[k]:
                self.structure[k][context_str] = Context()
            
            # Adiciona o caractere ao contexto
            if k == -1 and char != self.esc_symbol:
                # Remove do alfabeto no k=-1
                self.structure[-1]["NO_CONTEXT"].remove_character(char)
            else:
                # Adiciona ao contexto
                self.structure[k][context_str].add_character(char)
            
            # Verifica se o contexto está completo para remover o escape
            if k >= 0:
                context = self.structure[k][context_str]
                alphabet = set(["a", "b", "c", "d", "r"])
                if alphabet.issubset(context.get_characters()):
                    context.remove_character(self.esc_symbol)
    
    def decode_bits(self, bits: str, context_stack: List[str]) -> str:
        """
        Decodifica uma sequência de bits em um caractere usando o contexto atual.
        
        Args:
            bits: Sequência de bits a ser decodificada.
            context_stack: Pilha de contexto atual.
            
        Returns:
            O caractere decodificado.
        """
        # Tentativa de decodificar nos diferentes níveis de contexto
        for k in range(min(len(context_stack), self.k_max), -2, -1):
            if k > 0:
                context_str = ''.join(context_stack[:k])
            else:
                context_str = "NO_CONTEXT"
                
            # Obtém o contexto atual
            context = self.structure[k][context_str]
            
            # Reconstrói o dicionário de códigos
            codes = self.generate_codes(k, context_str)
            
            # Inverte o dicionário para mapear códigos para caracteres
            inv_codes = {code: char for char, code in codes.items()}
            
            # Verifica se o código corresponde a algum caractere
            if bits in inv_codes:
                return inv_codes[bits]
                
            # Se encontrar o símbolo de escape, continua para o próximo contexto
            if bits in [code for char, code in codes.items() if char == self.esc_symbol]:
                continue
                
        # Se não conseguir decodificar, retorna vazio
        return ""
    
    def decode_from_model(self, model: PPMModel, encoded_data: List[Tuple[str, int, str, str, Tuple[int, int]]]) -> str:
        """
        Decodifica usando um modelo PPM pré-existente.
        
        Args:
            model: Modelo PPM com a estrutura de dados.
            encoded_data: Lista de tuplas com os dados codificados.
            
        Returns:
            O texto decodificado.
        """
        self.structure = model.structure
        return self.decode_sequence(encoded_data) 