import heapq
import math
from collections import defaultdict

class Node:
    def _init_(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    def _lt_(self, other):
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

def build_huffman_tree(frequency_dict):
    # Ordenando o dicionário primeiro por cedilha, depois alfabeticamente e, por fim, pela frequência
    sorted_items = sorted(frequency_dict.items(), key=lambda x: (x[0], x[1])) 
    heap = [Node(char, freq) for char, freq in sorted_items]
    heapq.heapify(heap)
    print(f"Lista de nós antes da construção da árvore: {[f'({node.char}, {node.freq})' for node in heap]}")    

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)
        print(f"Unindo '{left.char}' e '{right.char}' com frequências {left.freq} e {right.freq} para formar '{merged.char}' com frequência {merged.freq}")

    return heap[0]

def generate_huffman_codes(node, prefix="", codebook={}):
    if node is not None:
        if node.char is not None:
            codebook[node.char] = prefix
        generate_huffman_codes(node.left, prefix + "0", codebook)
        generate_huffman_codes(node.right, prefix + "1", codebook)
    return codebook

def huffman_encoding(frequency_dict):
    if not frequency_dict:
        return {}
    
    tree_root = build_huffman_tree(frequency_dict)
    codes = generate_huffman_codes(tree_root)
    return codes

# Exemplo de uso:
frequency_dict = {"a": 5, "ç": 6, "b": 2, "r": 2, "c": 1, "d": 1, "e": 1}

ppm_structure = {
    -1: {
        "NO_CONTEXT": {
            "e": 1, "f": 1, "g": 1, "h": 1, "i": 1, "j": 1, "k": 1, "l": 1, "m": 1, "n": 1,
            "o": 1, "p": 1, "q": 1, "s": 1, "t": 1, "u": 1, "v": 1, "w": 1, "x": 1, "y": 1, "z": 1, "_": 1, "ç": 1
        }
    },
    0: {
        "NO_CONTEXT": {
            "a": 5, "ç": 6, "b": 2, "r": 2, "c": 1, "d": 1
        }
    }, 
    1: {
        "a": {"b": 2, "ç": 4, "c": 1, "d": 1},
        "b": {"r": 2, "ç": 1},
        "r": {"a": 2, "ç": 1},
        "c": {"a": 1, "ç": 1},
        "d": {"a": 1, "ç": 1}
    },
    2: {
        "ba": {"r": 2, "ç": 1},
        "rb": {"a": 2, "ç": 1},
        "ar": {"c": 1, "ç": 2},
        "ca": {"a": 1, "ç": 1},
        "ac": {"d": 1, "ç": 1},
        "da": {"a": 1, "ç": 1},
        "ad": {"b": 1, "ç": 1}
    }
}

frequency_dict = ppm_structure[0]["NO_CONTEXT"]

ignore_chars = [" ", "_", "\n", "b", "d"]

freq_dict = {}
freq_dict = {char: ppm_structure[0]["NO_CONTEXT"][char] for char in ppm_structure[0]["NO_CONTEXT"] if char not in ignore_chars}

print("Frequências:", freq_dict)

codes = huffman_encoding(frequency_dict)
print("Códigos de Huffman:", codes)

codes = huffman_encoding(freq_dict)
print("Códigos de Huffman:", codes)

frequency_dict = ppm_structure[-1]["NO_CONTEXT"]

codes = equiprovable_huffman(frequency_dict)
print("Códigos de Huffman:", codes)