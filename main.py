import heapq
import os
import sys


def shannon_fano(symbols_with_frequencies):
    """
    Algoritmo de codificação Shannon-Fano.
    """
    symbols_with_frequencies.sort(key=lambda x: x[1], reverse=True)

    def sf_split(symbols):
        if len(symbols) == 1:
            return {symbols[0][0]: ""}

        total = sum(freq for _, freq in symbols)
        cumulative = 0
        split_index = -1

        for i, (_, freq) in enumerate(symbols):
            if (cumulative + freq) >= total / 2:
                if abs((cumulative + freq - (total / 2))) < abs((cumulative - (total / 2))):
                    split_index = i
                else:
                    split_index = i - 1
                break
            cumulative += freq

        group1 = symbols[:split_index + 1]
        group2 = symbols[split_index + 1:]

        codes = {}
        for symbol, code in sf_split(group1).items():
            codes[symbol] = "0" + code
        for symbol, code in sf_split(group2).items():
            codes[symbol] = "1" + code

        return codes

    return sf_split(symbols_with_frequencies)


def compress(text, codes):
    """Converte o texto em um código binário mínimo usando a codificação Shannon-Fano."""
    str_code = ''.join(codes[char] for char in text if char in codes)
    print("CODIFICADO: ", str_code)
    print(len(str_code))

    sum = len(str_code) % 8
    sum = 8 - sum
    print(sum)

    for _ in range(sum):
        str_code += "0"

    # Transformar a string binária em blocos de 8 bits
    with open('compress.bin', 'wb') as f:
        for i in range(0, len(str_code), 8):
            byte_str = str_code[i:i+8]  # Pega 8 bits da string
            byte = int(byte_str, 2)  # Converte para inteiro
            f.write(bytes([byte]))  # Escreve no arquivo como byte
    return sum


def decodifica_arquivo(tamamanho_do_codigo):
    # Lê o arquivo binário
    with open('compress.bin', 'rb') as f:
        # Lê todo o conteúdo do arquivo como bytes
        content = f.read()

        # Imprime o conteúdo em forma de binário
        binary_content = ''.join(format(byte, '08b') for byte in content)
        print("DECODIFICADO: ", binary_content[:len(
            binary_content)-tamamanho_do_codigo])
        return binary_content


def decompress(binary_code, codes):
    """Descomprime um código binário de volta ao texto original."""
    reverse_codes = {v: k for k, v in codes.items()}
    decoded_text = ""
    temp_code = ""
    binary_str = binary_code
    for bit in binary_str:
        temp_code += bit
        if temp_code in reverse_codes:
            decoded_text += reverse_codes[temp_code]
            temp_code = ""
    return decoded_text


def calculate_compression_ratio(texto_original, codigo_binario):
    # Número total de bits após compressão
    total_bits = len(codigo_binario)

    # Número de símbolos na mensagem original
    numero_simbolos = len(texto_original)

    # Número médio de bits por símbolo
    numero_medio_bits_por_simbolo = total_bits / numero_simbolos

    # Calcular a razão de compressão
    razao_compressao = 5 / numero_medio_bits_por_simbolo

    return razao_compressao


def save_to_file(filename, content):
    """Salva o conteúdo em um arquivo."""
    with open(filename, "wb") as file:
        file.write(content)


# Frequências fornecidas
symbols_with_frequencies = [
    (' ', 17.00), ('E', 14.63), ('A', 13.72), ('O', 10.73), ('S', 7.81),
    ('R', 6.53), ('I', 6.18), ('N', 5.05), ('D', 4.99), ('M', 4.74),
    ('U', 4.63), ('T', 4.34), ('C', 3.88), ('L', 2.78), ('P', 2.52),
    ('V', 1.67), ('G', 1.30), ('H', 1.28), ('Q', 1.20), ('B', 1.04),
    ('F', 1.02), ('Z', 0.47), ('J', 0.40), ('X', 0.27), ('K', 0.02),
    ('W', 0.01), ('Y', 0.01)
]

# Gerar códigos Shannon-Fano
codes = shannon_fano(symbols_with_frequencies)

# Exemplo de compressão e descompressão
original_text = "LUCAS FREITAS BITU CRATO CEARA"
tamamanho_do_codigo = compress(original_text, codes)
compressed_text = decodifica_arquivo(tamamanho_do_codigo)
decompressed_text = decompress(compressed_text, codes)

save_to_file("original.txt", original_text.encode())

# Calcular razão de compressão
compression_ratio = calculate_compression_ratio(original_text, compressed_text)

# Resultados
print("Códigos Shannon-Fano:")
for symbol, code in codes.items():
    print(f"{symbol}: {code}")

print("\nTexto original:", original_text)
print("Texto comprimido:", compressed_text)
print("Texto descomprimido:", decompressed_text)
print("Razão de compressão:", compression_ratio)
