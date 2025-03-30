import heapq
import math
from collections import defaultdict

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.freq < other.freq

def equiprovable_huffman(frequency_dict):
    # Ordenar as chaves alfabéticas, mas sem considerar o cedilha primeiro
    sorted_items = sorted(frequency_dict.items(), key=lambda x: (x[0], x[1]))

    # Número de caracteres distintos
    num_chars = len(sorted_items)

    # Calcular o número de bits necessários para representar todos os caracteres
    code_length = math.ceil(math.log2(num_chars))

    # Gerar os códigos binários de comprimento fixo
    codes = {char: format(i, f'0{code_length}b') for i, (char, _) in enumerate(sorted_items)}

    return codes

def build_huffman_tree(frequency_dict, verbose=True):
    # Ordenando o dicionário primeiro por cedilha, depois alfabeticamente e, por fim, pela frequência
    sorted_items = sorted(frequency_dict.items(), key=lambda x: (x[0], x[1])) 
    heap = [Node(char, freq) for char, freq in sorted_items]
    heapq.heapify(heap)
    
    if verbose:
        print(f"Lista de nós antes da construção da árvore: {[f'({node.char}, {node.freq})' for node in heap]}")    

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)
        
        if verbose:
            print(f"Unindo '{left.char}' e '{right.char}' com frequências {left.freq} e {right.freq} para formar '{merged.char}' com frequência {merged.freq}")

    return heap[0]

def generate_huffman_codes(node, prefix="", codebook={}):
    if node is not None:
        if node.char is not None:
            codebook[node.char] = prefix
        generate_huffman_codes(node.left, prefix + "0", codebook)
        generate_huffman_codes(node.right, prefix + "1", codebook)
    return codebook

def huffman_encoding(frequency_dict, verbose=True):
    if not frequency_dict:
        return {}
    
    tree_root = build_huffman_tree(frequency_dict, verbose)
    codes = generate_huffman_codes(tree_root, "", {})
    return codes

def codificar_ppm(ppm_structure, k, context, char, ignore_chars, verbose=False):
    # Implementação da decodificação PPM (não fornecida no código original)
    freq_dict = {}
    
    if len(freq_dict) == 1:
            # Se o dicionário estiver vazio, retorna None
            return None
        
    if k == -1:

        contexts_dict = ppm_structure[k]["NO_CONTEXT"].char_counts
        codes = equiprovable_huffman(contexts_dict)
    elif k == 0:
        contexts_dict = ppm_structure[k]["NO_CONTEXT"].char_counts
            
        freq_dict = {c: count for c, count in contexts_dict.items() if c not in ignore_chars}
        codes = huffman_encoding(freq_dict, verbose)
    else:
        contexts_dict = ppm_structure[k][context].char_counts
            
        freq_dict = {c: count for c, count in contexts_dict.items() if c not in ignore_chars}
        codes = huffman_encoding(freq_dict, verbose)

    return codes.get(char, None)

