from typing import Dict, Set

def huffman_decoding(codes: Dict[str, str], bits: str) -> str:
    """
    Decodifica uma sequência de bits usando códigos Huffman.
    
    Args:
        codes: Dicionário de códigos Huffman (caractere -> código).
        bits: Sequência de bits a ser decodificada.
        
    Returns:
        O caractere decodificado ou None se não encontrado.
    """
    # Inverter o dicionário de códigos (código -> caractere)
    inv_codes = {code: char for char, code in codes.items()}
    
    # Procurar o código correspondente
    return inv_codes.get(bits, None)

def codificar_para_ppm(ppm_structure, k, context, bits, verbose=False):
    """
    Converte bits para um caractere usando a estrutura PPM.
    
    Args:
        ppm_structure: Estrutura de dados do PPM.
        k: Nível do contexto.
        context: String de contexto.
        bits: Bits a serem decodificados.
        verbose: Se True, imprime informações detalhadas.
        
    Returns:
        O caractere correspondente aos bits ou None se não encontrado.
    """
    if k == -1:
        contexts_dict = ppm_structure[k]["NO_CONTEXT"].char_counts
        # Usando equiprovável para k=-1
        from utils.encoder import equiprovable_huffman
        codes = equiprovable_huffman(contexts_dict)
    else:
        if context not in ppm_structure[k]:
            return None
            
        contexts_dict = ppm_structure[k][context].char_counts
        # Usando Huffman para outros contextos
        from utils.encoder import huffman_encoding
        codes = huffman_encoding(contexts_dict, verbose)
    
    # Inverter os códigos para decodificação
    inv_codes = {code: char for char, code in codes.items()}
    
    if verbose:
        print(f"Decodificando bits '{bits}' no contexto {k}:{context}")
        print(f"Códigos disponíveis: {inv_codes}")
        
    return inv_codes.get(bits, None) 