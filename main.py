def shannon_fano(symbols_with_frequencies):
    """
    Algoritmo de codificação Shannon-Fano.

    Args:
        symbols_with_frequencies (list of tuples): Uma lista de tuplas (símbolo, frequência).

    Returns:
        dict: Um dicionário que mapeia cada símbolo para seu código Shannon-Fano.
    """
    # Ordena os símbolos por frequência em ordem decrescente
    symbols_with_frequencies.sort(key=lambda x: x[1], reverse=True)

    def sf_split(symbols):
        """Divide recursivamente os símbolos e atribui códigos."""
        if len(symbols) == 1:
            # Caso base: símbolo único, sem código ainda
            return {symbols[0][0]: ""}

        # Encontra o ponto de divisão para equilibrar as frequências
        total = sum(freq for _, freq in symbols)
        cumulative = 0
        split_index = -1

        for i, (_, freq) in enumerate(symbols):
            cumulative += freq
            if cumulative >= total / 2:
                split_index = i
                break

        # Divide em dois grupos
        group1 = symbols[:split_index + 1]
        group2 = symbols[split_index + 1:]

        # Atribui códigos recursivamente
        codes = {}
        for symbol, code in sf_split(group1).items():
            codes[symbol] = "1" + code
        for symbol, code in sf_split(group2).items():
            codes[symbol] = "0" + code

        return codes

    # Inicia a divisão recursiva e retorna os códigos resultantes
    return sf_split(symbols_with_frequencies)


def decode_shannon_fano(encoded_data, code_tree):
    """
    Decodifica dados codificados usando a árvore de códigos Shannon-Fano.

    Args:
        encoded_data (str): Dados codificados como uma sequência de bits.
        code_tree (dict): O dicionário de códigos Shannon-Fano.

    Returns:
        str: A mensagem decodificada.
    """
    # Constrói a árvore de decodificação a partir do dicionário de códigos
    decoding_tree = {}
    for symbol, code in code_tree.items():
        current_node = decoding_tree
        for bit in code:
            if bit not in current_node:
                current_node[bit] = {}
            current_node = current_node[bit]
        current_node['symbol'] = symbol

    # Decodifica os dados bit a bit
    decoded_message = []
    current_node = decoding_tree
    for bit in encoded_data:
        current_node = current_node[bit]
        if 'symbol' in current_node:
            decoded_message.append(current_node['symbol'])
            current_node = decoding_tree

    return ''.join(decoded_message)


def encode_shannon_fano(message, code_tree):
    """
    Codifica uma mensagem usando o dicionário de códigos Shannon-Fano.

    Args:
        message (str): A mensagem a ser codificada.
        code_tree (dict): O dicionário de códigos Shannon-Fano.

    Returns:
        str: A mensagem codificada como uma sequência de bits.
    """
    encoded_message = []
    for symbol in message:
        if symbol in code_tree:
            encoded_message.append(code_tree[symbol])
        else:
            raise ValueError(
                f"Símbolo '{symbol}' não encontrado no código Shannon-Fano.")
    return ''.join(encoded_message)


# Exemplo de uso
symbols_with_frequencies = [
    ('Espaço', 17.00), ('E', 14.63), ('A', 13.72), ('O', 10.73),
    ('S', 7.81), ('R', 6.53), ('I', 6.18), ('N', 5.05),
    ('D', 4.99), ('M', 4.74), ('U', 4.63), ('T', 4.34),
    ('C', 3.88), ('L', 2.78), ('P', 2.52), ('V', 1.67),
    ('G', 1.30), ('H', 1.28), ('Q', 1.20), ('B', 1.04),
    ('F', 1.02), ('Z', 0.47), ('J', 0.40), ('X', 0.27),
    ('K', 0.02), ('W', 0.01), ('Y', 0.01)
]
codes = shannon_fano(symbols_with_frequencies)
print("Códigos Shannon-Fano:")
for symbol, code in codes.items():
    print(f"{symbol}: {code}")

# Mensagem a ser codificada
message = "ESPACO"
encoded_message = encode_shannon_fano(message, codes)
print("Mensagem codificada:", encoded_message)

# Decodificação de exemplo
encoded_data = "110011011010"  # Exemplo de dados codificados (bits)
decoded_message = decode_shannon_fano(encoded_data, codes)
print("Mensagem decodificada:", decoded_message)
